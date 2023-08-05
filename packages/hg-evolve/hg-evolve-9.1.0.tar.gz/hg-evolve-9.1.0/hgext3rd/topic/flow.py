from __future__ import absolute_import

from mercurial import (
    commands,
    error,
    exchange,
    extensions,
    node,
    phases,
)

from mercurial.i18n import _

from . import (
    compat,
)

def enforcesinglehead(repo, tr):
    branchmap = repo.filtered('visible').branchmap()
    for name, heads in compat.branchmapitems(branchmap):
        if len(heads) > 1:
            hexs = [node.short(n) for n in heads]
            raise error.Abort(_('%d heads on "%s"') % (len(heads), name),
                              hint=(', '.join(hexs)))

def publishbarebranch(repo, tr):
    """Publish changeset without topic"""
    if 'node' not in tr.hookargs: # no new node
        return
    startnode = node.bin(tr.hookargs['node'])
    topublish = repo.revs('not public() and (%n:) - hidden() - topic()', startnode)
    if topublish:
        cl = repo.changelog
        nodes = [cl.node(r) for r in topublish]
        repo._phasecache.advanceboundary(repo, tr, phases.public, nodes)

def rejectuntopicedchangeset(repo, tr):
    """Reject the push if there are changeset without topic"""
    if 'node' not in tr.hookargs: # no new revs
        return

    startnode = node.bin(tr.hookargs['node'])

    mode = repo.ui.config('experimental', 'topic-mode.server', 'ignore')

    untopiced = repo.revs('not public() and (%n:) - hidden() - topic()', startnode)
    if untopiced:
        num = len(untopiced)
        fnode = repo[untopiced.first()].hex()[:10]
        if num == 1:
            msg = _("%s") % fnode
        else:
            msg = _("%s and %d more") % (fnode, num - 1)
        if mode == 'warning':
            fullmsg = _("pushed draft changeset without topic: %s\n")
            repo.ui.warn(fullmsg % msg)
        elif mode == 'enforce':
            fullmsg = _("rejecting draft changesets: %s")
            raise error.Abort(fullmsg % msg)
        else:
            repo.ui.warn(_("unknown 'topic-mode.server': %s\n" % mode))

def reject_publish(repo, tr):
    """prevent a transaction to be publish anything"""
    published = set()
    for r, (o, n) in tr.changes['phases'].items():
        if n == phases.public:
            published.add(r)
    if published:
        r = min(published)
        msg = "rejecting publishing of changeset %s" % repo[r]
        if len(published) > 1:
            msg += ' and %d others' % (len(published) - 1)
        raise error.Abort(msg)

def wrappush(orig, repo, remote, *args, **kwargs):
    """interpret the --publish flag and pass it to the push operation"""
    newargs = kwargs.copy()
    if kwargs.pop('publish', False):
        opargs = kwargs.get('opargs')
        if opargs is None:
            opargs = {}
        newargs['opargs'] = opargs.copy()
        newargs['opargs']['publish'] = True
    return orig(repo, remote, *args, **newargs)

def extendpushoperation(orig, self, *args, **kwargs):
    publish = kwargs.pop('publish', False)
    orig(self, *args, **kwargs)
    self.publish = publish

def wrapphasediscovery(orig, pushop):
    orig(pushop)
    if getattr(pushop, 'publish', False):
        if not pushop.remotephases.publishing:
            unfi = pushop.repo.unfiltered()
            droots = pushop.remotephases.draftroots
            revset = '%ln and (not public() or %ln::)'
            future = list(unfi.set(revset, pushop.futureheads, droots))
            pushop.outdatedphases = future

def installpushflag(ui):
    entry = extensions.wrapcommand(commands.table, 'push', wrappush)
    if not any(opt for opt in entry[1] if opt[1] == 'publish'): # hg <= 4.9
        entry[1].append(('', 'publish', False,
                         _('push the changeset as public')))
    extensions.wrapfunction(exchange.pushoperation, '__init__',
                            extendpushoperation)
    extensions.wrapfunction(exchange, '_pushdiscoveryphase', wrapphasediscovery)
    exchange.pushdiscoverymapping['phase'] = exchange._pushdiscoveryphase

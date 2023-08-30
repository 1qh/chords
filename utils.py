def dsort(d):
    return dict(sorted(d.items())).items()


def export(l):
    with open('_.txt', 'w') as f:
        f.write('\n'.join(l))

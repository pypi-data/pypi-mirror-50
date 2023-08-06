from colr import Colr as C

c = C('\n').join(
    C('test', 'red').blue(' this').green('out')('.'),
    C().rgb(25, 34, 35, text='testing'),
    C().hex('#ffffff', text='okay?')
)
print('Colr: {}'.format(c))
print('\n'.join(
    f'{p!r} {p.code_type}: {p.code_name}'
    for p in c.parts()
))

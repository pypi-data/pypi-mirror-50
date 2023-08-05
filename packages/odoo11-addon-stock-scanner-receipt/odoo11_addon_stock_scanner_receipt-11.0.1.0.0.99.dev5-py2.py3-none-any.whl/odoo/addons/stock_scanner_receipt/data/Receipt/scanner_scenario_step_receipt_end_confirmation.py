# flake8: noqa
'Use <m> or <message> to retrieve the data transmitted by the scanner.'
'Use <t> or <terminal> to retrieve the running terminal browse record.'
'Put the returned action code in <act>, as a single character.'
'Put the returned result or message in <res>, as a list of strings.'
'Put the returned value in <val>, as an integer'

picking = model.browse(terminal.reference_document)

act = 'C'
res = [
    _('Do you really want to terminate this receipt?'),
]

if not any(picking.move_line_ids.filtered(lambda x: not x.move_id)):

    act = 'A'
    val = True

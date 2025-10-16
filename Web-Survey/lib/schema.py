from lxml import etree

class QDetails:
    def __init__(self):
        self.qtext = ''
        self.options = []
        self.option_ids = []
        self.qtype = ''
    def get_xml(self, qre, qn):
        qre_ = etree.parse(qre).getroot()
        opts = []
        opts_id = []
        for item in qre_.iter():
            id_ = item.get('id')
            if id_ == qn:
                self.qtype = item.get('type')
                self.qtext = item.text
                if self.qtype in ['single', 'multi', 'grid']:
                    for option in qre_.xpath('//question[@id="'+qn+'"]/option'):
                        opts.append(option.text)
                        opts_id.append(option.get('id'))
                else:
                    self.options = None
        self.options = opts
        self.option_ids = opts_id

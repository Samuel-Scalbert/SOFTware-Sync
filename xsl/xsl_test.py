from lxml import etree

# Load XML document
xml = etree.parse('./data/xml_files/PMC3130168.xml')

# Load XSLT stylesheet
xslt = etree.parse('./xsl/text.xslt')
transform = etree.XSLT(xslt)

# Apply transformation
result = transform(xml)

# Output the result
print(result)

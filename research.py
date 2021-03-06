#!/usr/bin/python
# -*- coding: utf-8 -*-

import io, sys, re, os
from glob import glob


files = glob("research/*.html")

article_template = """	<li>
		<h2><a href="**link**">**title**</a></h2>
		<div class="research_blob">
			<div class="research_img_float">
				<img src="images/**img**" width="280" alt="**title**">
			</div>
			<p class="research_lead">**lead**</p>
			<a class="button small" href="**link**">More</a>
		</div>
"""

page_template = """<section class="research">
									<header class="main">
										<h1>Research</h1>
									</header>
									<ul style="list-style-type:none">
											**content**
									</ul>
					</section>"""

output = ""

for infile in files:
	if "template" not in infile:
		text = io.open(infile,encoding="utf8").read()
		filename = os.path.basename(infile)

		m = re.search(r'<h1>(.*?)</h1>',text,re.MULTILINE|re.DOTALL)
		if m is None:
			continue
		else:
			h1 = m.group(1).replace("<br>","").replace("<br/>","")

		#sys.stdout.write("found: "+ h1)

		m = re.search(r'<span class="image main">.*?src="[^"]*?images/([^"]+)".*?</span>.*?<p>(.*?)</p>',text,re.MULTILINE|re.DOTALL)
		if m is None:
			continue
		else:
			img_src = m.group(1)
			first_para = m.group(2)
		#sys.stdout.write("found: "+ img_src)

		article = article_template.replace("**title**",h1).replace("**img**",img_src).replace("**link**","research/"+filename).replace("**lead**",first_para)

		output += article

output = page_template.replace("**content**",output)

print("Content-type:text/html\r\n\r\n")
print(output.encode("utf8"))
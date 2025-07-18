# CIN Census csv and xml generator

This repository contains a generator for creating fake CIN Census xml files.

It does so in two stages:
- generate_csvs.py: this module has the function to create a set of csvs that correspond to the nested structures of the CIN Census XML file. You can set inputs like the number of children to be generated and the likelihood of certain events happening. The output is 10 csvs that correspond to the xml modules
- generate_xml.py: this module takes the csvs generated and creates a single xml file in the format of the CIN Census

# Why csvs and xmls?

I find it cumbersome reading over an xml and I wanted a quick way to review whether there were differences between the input XML and the output flatfile created by the liia-tools-pipeline cin pipeline. I use the csvs in order to make this quick comparison.

# How does it work?

- It uses poetry to manage dependencies
- Run poetry install to create an environment
- The script in main allows you to run either the csv generator or the xml generator
- There is a manual toggle in the main.py file to switch between the two
- Choose the setting you want and then:
- Run: poetry run python src/cin_xml_from_csv/main.py
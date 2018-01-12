"""empty message

Revision ID: 526dd67fe13a
Revises: 4203df2d0ccb
Create Date: 2017-12-21 10:31:09.343477

"""

# revision identifiers, used by Alembic.
revision = '526dd67fe13a'
down_revision = '4203df2d0ccb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    sql = """
    UPDATE public.pages_translation
   SET  text='## Welcome to Vision Diagnostic for Fluid Insulated Equipment. <a href="https://github.com/SnowBeaver/Vision" target="_blank"  style="float:right; color:#000; font-size:44px"><i class="fa fa-github" aria-hidden="true"></i></a>

### Introduction

Vision Diagnostic for Oil Insulated Equipment is an application devised to help power plant personnel to maintain in good condition equipment of electrical power netwrok, particularly transformers, circuit breakers and tap-changers. Vision Diagnostic for Oil Insulated Equipment will be useful to you for the maintenance of your mineral oil insulated equipment and the diagnosis of latent defects.
Vision Diagnostic for Oil Insulated Equipment is intended for companies who wish to carry out a consistent follow-up of their equipment. This software is a diagnosis tool for general use. It allows you to follow all the lab. results and carry out a complete diagnosis. The analysis, which follows, will allow you to track the apparatus that seems to deviate from the normal. From that moment, the maintenance personnel of the plant can take the appropriate decisions to maintain the plant equipment in good working order.
The software objective will not replace the knowledge of experts. On the contrary, their services must be retained to validate conclusions and suggest appropriate action for the circumstances. The intent of this software is to help and take in hand preventive maintenance of your power network apparatus by offering a diagnosis upon demand.
We would like to point out the apparent ease with which the software Vision Diagnostic for Oil Insulated Equipment can interpret your data. The interpretation of the elements of data, leading to a diagnosis and a recommendation, necessitates a general knowledge of insulating fluid filled equipment. This knowledge of the equipment should by preference, extend to the internal as well as external elements. It is also preferable to have a basic knowledge of the analysis of the physical properties of the insulated fluid, dissolved gases and electrical tests (TTR, dissipation factor, etc.). If the diagnosis techniques are not familiar to you, we recommend that you submit your data for a second opinion. In order to help you with this procedure, the software allows the information of selected apparatus to be export, so that a colleague can consult the corresponding data.

### Vision Diagnostic for Oil Insulated Equipment functions

The software Vision Diagnostic for Oil Insulated Equipment is composed of an operation window where one can have access to different elements of the application.
Vision Diagnostic for Oil Insulated Equipment is a follow-up and analysis tool. It detects the presence and type of latent fault inside equipment. Also, it allows for an increase in the useful life of transformers by the surveillance of the physical properties.
Vision Diagnostic for Oil Insulated Equipment allows for following and analyzing dissolved gases in the insulated fluid. With the help of tendencies method, key gases, ROGER\"S ratios, content of dissolved gases, carbonic gases and the electrical tests, we can determine the presence of a defect, its nature and its gravity.
Vision Diagnostic for Oil Insulated Equipment attends to the follow-up and evaluation of the physical properties of the oil and the insulation. It is therefore possible to increase the life expectancy of the transformer thanks to the maintenance of the insulating fluid properties.
All the diagnoses are accompanied by recommendations allowing you to orient your priorities so that you can plan your efforts to fit the latter within your preventive maintenance program.

### Description of characteristics

The user interface permits easy access to different software elements. Online help allows the user to follow the utilization steps of the software to support the interface.
The software is responsible for maintaining the data in a database format. This function is performed automatically, allowing the user to concentrate on the analysis of the information instead of the management of the database. This database allows you to keep information on the equipment, the type of sampling, the laboratory results, the electrical tests, the visual inspection, and the diagnosis. We have included comments fields, allowing you to take reminder notes on the sampling and the repairs. We have included a field doubtful condition, abbreviated to DC, to locate rapidly the apparatus in need of follow-up.
The software allows for visualizing data on a unit in graph or spreadsheet form. While the graph format allows for a quick glance to note development of abnormalities in the characteristics of the oil insulated equipment, the spreadsheet shows all the numerical data formatted in lines and columns as supplied by the laboratory. The data may also be printed as a report.
Vision Diagnostic for Oil Insulated Equipment functions on a network. Several users can access the database of your oils. In order to control access to the information, you have the possibility to define a password and an access profile for as many users as necessary. Users can be assign different profile to fit their responsabilities.
To make a diagnosis of a large quantity of units easier, we have incorporated a batch processing of data to generate a diagnosis of the equipment. This function increases the efficiency of the analysis. In batch processing, units in doubtful conditions are indicated in the DC field, in this way you can establish your priorities rapidly.
Vision Diagnostic for Oil Insulated Equipment carries out a follow-up of the relative humidity in the paper.
Vision Diagnostic for Oil Insulated Equipment makes a correlation between your gas Transducer, if your transformer is equipped with one, and from the laboratory results.

The software contains a vast range of information on the subject of the fluid insulated units as well as on the interpretation of insulating fluid analysis results.

<img src="../app/static/img/screen_2.png" width="540px" style="padding:5px; border:1px solid #BBB"/> <img src="../app/static/img/screen_1.png" width="540px" style="padding:5px; border:1px solid #BBB; float:right"/>' where id=3 and locale='en'

    """
    op.execute(sql=sql)
    pass


def downgrade():
    sql = """
    
    UPDATE public.pages_translation
   SET  text='
###Welcome to Vision Diagnostic for Fluid Insulated Equipment.
###Introduction
This site is for users who wants to perform fluid insulated equipment diagnostic. It is free to use and the site can be copied to your own computer or server. Instructions are given to do that.

Anyone can use it, there is no restriction. Any suggestions are welcome: diagnostic, new tools, etc..

At the moment we are working at enabling different tools that make the structure of this site. The site is coded exclusively in Python. We stayed away from the traditional mixes of language: PHP, DJANGO, etc.. to use only one. The site code becomes much easier to maintain this way. We also uses Python version 3.x, making it open to any future upgrade.

###Site structure
We want to keep the site lean, so any user manual and technical information will be maintain in self-contain areas. You can find links to all material in the Wiki.' where id=3 and locale='en'
"""
    op.execute(sql=sql)
    pass

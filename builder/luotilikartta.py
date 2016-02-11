#!Python3
#--*-- coding:utf-8 --*--

import xml.etree.ElementTree as ET



root = ET.Element("odoo")
data = ET.SubElement(root,"data",{'noupdate':'1'})

TEMPLATEID="finnish_scouting_chart_template"

def record(parent,cid,model="account.account.template"):
    return ET.SubElement(parent,'record',{ 'id':cid,'model':model})

def field(parent,name,value,ref=None,xeval=None):
    y={'name':name}
    if ref:
        y['ref']=ref
    if xeval:
        y['eval']=xeval
    x=ET.SubElement(parent,'field',y)
    if value:
        x.text=value
    return x


#<record id="austria_chart_template" model="account.chart.template">
#    <field name="name">Finland - Local Scout Group Accounting</field>
#    <field name="code_digits">4</field>
#    <field name="bank_account_code_prefix">201</field><!-- 2800-->
#    <field name="cash_account_code_prefix">202</field><!-- 2700 -->
#    <field name="currency_id" ref="base.EUR"/>
#    <field name="transfer_account_id" ref="transfer_account_id"/>
#    </record>

def domainrec(tid):
    mainrec=record(data,TEMPLATEID,model="account.chart.template")
    nf=field(mainrec,'name','Finland - Local Scout Group Accounting')
    nf2=field(mainrec,'code_digits','4')
    nf3=field(mainrec,'bank_account_code_prefix','101')
    nf4=field(mainrec,'cash_account_code_prefix','100')
    nf5=field(mainrec,'currency_id',None,ref='base.EUR')
    nf5=field(mainrec,'transfer_account_id',None,ref='a'+tid)


for rivi in open('tilikartta.csv','r',encoding='iso8859-1'):
    rivi=rivi.strip()
    palat=rivi.split(";")
    if len(palat)==2 or len(palat)==3 or len(palat)==4:
        reconcile=False
        trasferaccount=False
        if len(palat)==2:
            selitys,tyyppi=palat
        elif len(palat)==3:
            selitys,tyyppi,rec=palat
            if rec=="1":
                reconcile=True
        else:
            selitys,tyyppi,rec,transfer=palat
            if rec=="1":
                reconcile=True
            if transfer=="1":
                trasferaccount=True
        selitys=selitys.strip()
        tyyppi=tyyppi.strip()
        code=selitys[:3]
        if not code.isdigit():
            continue
        if trasferaccount:
            tid=code
        selitys=selitys[3:].strip()
        acc1=record(data,'a'+code)
        fcode=field(acc1,'code',code)
        fcode=field(acc1,'name',selitys)
        if not trasferaccount:
            fid=field(acc1,'chart_template_id',None,ref=TEMPLATEID)
        ftyp=field(acc1,'user_type_id',None,ref="account."+tyyppi)
        if reconcile:
            frec=field(acc1,'reconcile',None,xeval='True')
        if trasferaccount:
            domainrec(code);
            acc2=record(data,'a'+code)
            fid=field(acc2,'chart_template_id',None,ref=TEMPLATEID)

        
ET.dump(root)
tree= ET.ElementTree(element=root)
tree.write(r"..\account_chart.xml",encoding="utf-8",xml_declaration=True)
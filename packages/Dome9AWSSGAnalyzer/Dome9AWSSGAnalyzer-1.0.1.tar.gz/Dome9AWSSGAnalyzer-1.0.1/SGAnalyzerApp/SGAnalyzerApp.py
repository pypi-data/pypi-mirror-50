# SGAnalyzerApp - gui

# importing modules required to run
from tkinter import *
import json
import time
from SGAnalyzerAppDir.SGAnalyzerApp import Dome9SG


def app():

    # creating root object
    root = Tk()

    root.geometry("840x270")

    root.title("Dome9-SG-LookUp")
    root.resizable(0, 0)

    Tops = Frame(root, width=180, relief=RIDGE)
    Tops.pack(side=TOP)

    f1 = Frame(root, width=170, height=150, relief=RIDGE)
    f1.pack(side=LEFT)

    # Set String Vars
    external_Id = StringVar()
    security_Group_Name = StringVar()
    description = StringVar()
    vpc_Id = StringVar()
    region_Id = StringVar()
    cloud_Account_Name = StringVar()
    AWS_AC_ID = StringVar()

    # Function to reset the window
    def reset():
        external_Id.set("")
        security_Group_Name.set("")
        description.set("")
        vpc_Id.set("")
        region_Id.set("")
        cloud_Account_Name.set("")
        AWS_AC_ID.set("")

    # Function for not getting SG
    def not_found():
        security_Group_Name.set("Not Found")
        description.set("Not Found")
        vpc_Id.set("Not Found")
        region_Id.set("Not Found")
        cloud_Account_Name.set("Not Found")
        AWS_AC_ID.set("Not Found")

    def get_sg_details():
        """ Get SG Details in GUI box when only SGID is provided """
        check = external_Id.get()
        if not check.strip():
            external_Id.set("Enter Valid string!!!")
        else:
            obj = Dome9SG(sg_id=external_Id.get())
            sg_details_json = obj.get_sg_by_id()
            if "Result" in sg_details_json.keys():
                not_found()
            else:
                security_Group_Name.set(sg_details_json["securityGroupName"])
                description.set(sg_details_json["description"])
                vpc_Id.set(sg_details_json["vpcId"])
                region_Id.set(sg_details_json["regionId"])
                cloud_Account_Name.set(sg_details_json["cloudAccountName"])
                AWS_AC_ID.set(obj.aws_dome9map[sg_details_json["cloudAccountId"]])

    def get_sg_rules():
        """ Download SGRules in JSON when only SGID is provided """
        """ Format: SGRules_sg-abcd1234_FriAug21922112019"""
        check = external_Id.get()
        if not check.strip():
            external_Id.set("Enter Valid string!!!")
        else:
            sg_details_json = Dome9SG(sg_id=external_Id.get()).get_sg_by_id()
            if "Result" in sg_details_json.keys():
                not_found()
            else:
                service_rules = sg_details_json["services"]
                filename = 'SGRules_' + sg_details_json["externalId"] + "_" + \
                           str(time.asctime(time.localtime(time.time()))).replace(":", "").replace(" ", "") \
                           + '.json'
                with open(filename, 'w', encoding='utf-8') as j:
                    json.dump(service_rules, j, ensure_ascii=False, indent=4)

    def get_sg_by_name():
        """ Download all SGs with SGDetails in json when SGName is provided """
        """ Format: SGMatches_SG-DC_FriAug21923162019.json """
        check = security_Group_Name.get()
        if not check.strip():
            security_Group_Name.set("Enter Valid string!!!")
        else:
            sg_details_json = Dome9SG(sg_name=security_Group_Name.get()).get_all_sg_by_name()
            if len(sg_details_json) == 0:
                not_found()
            filename = 'SGMatches_' + security_Group_Name.get() + "_" + \
                       str(time.asctime(time.localtime(time.time()))).replace(":", "").replace(" ", "") \
                       + '.json'
            with open(filename, 'w', encoding='utf-8') as j:
                json.dump(sg_details_json, j, ensure_ascii=False, indent=4)

    # Title
    lblTitle = Label(Tops, font=('helvetica', 10, 'bold'), text="Sec Ops SG Analyzer",
                     fg="Black", bd=5, anchor='w')
    lblTitle.grid(row=0, column=2)
    lblTitle2 = Label(Tops, font=('arial', 10, 'bold'), text=time.asctime(time.localtime(time.time())),
                      fg="Steel Blue", bd=5, anchor='w')
    lblTitle2.grid(row=1, column=2)

    # SGId
    lblSGId = Label(f1, font=('arial', 10, 'bold'), text="SGID (Required):", bd=5, anchor="w")
    lblSGId.grid(row=0, column=2)
    txtSGId = Entry(f1, font=('arial', 10, 'bold'), textvariable=external_Id, bd=5, insertwidth=4, bg="powder blue",
                    justify='right')
    txtSGId.grid(row=0, column=3)


    # AccountNumber
    lblACNo = Label(f1, font=('arial', 10, 'bold'), text="Account Number:", bd=5, anchor="w")
    lblACNo.grid(row=0, column=0)
    txtACNo = Entry(f1, font=('arial', 10, 'bold'), textvariable=AWS_AC_ID, bd=5, insertwidth=4, bg="powder blue",
                    justify='right')
    txtACNo.grid(row=0, column=1)


    # RegionId
    lblRegId = Label(f1, font=('arial', 10, 'bold'), text="Region :", bd=5, anchor="w")
    lblRegId.grid(row=0, column=4)
    txtRegId = Entry(f1, font=('arial', 10, 'bold'), textvariable=region_Id, bd=5, insertwidth=4, bg="powder blue",
                     justify='right')
    txtRegId.grid(row=0, column=5)

    # SGName
    lblSGName = Label(f1, font=('arial', 10, 'bold'), text="SGName(Required):", bd=10, anchor="w")
    lblSGName.grid(row=1, column=2)
    txtSGName = Entry(f1, font=('arial', 10, 'bold'), textvariable=security_Group_Name, bd=5, insertwidth=4,
                      bg="powder blue", justify='right')
    txtSGName.grid(row=1, column=3)

    # AccountName
    lblACN = Label(f1, font=('arial', 10, 'bold'), text="Account Name:", bd=10, anchor="w")
    lblACN.grid(row=1, column=0)
    txtACN = Entry(f1, font=('arial', 10, 'bold'),
                   textvariable=cloud_Account_Name, bd=5, insertwidth=4,
                   bg="powder blue", justify='right')
    txtACN.grid(row=1, column=1)

    # VPC-ID
    lblVPCId = Label(f1, font=('arial', 10, 'bold'), text="VPC-ID:", bd=10, anchor="w")
    lblVPCId.grid(row=1, column=4)
    txtVPCId = Entry(f1, font=('arial', 10, 'bold'), textvariable=vpc_Id, bd=5, insertwidth=4, bg="powder blue",
                     justify='right')
    txtVPCId.grid(row=1, column=5)

    # SGDescription
    lblSGDesc = Label(f1, font=('arial', 10, 'bold'), text="SG Description:", bd=10, anchor="w")
    lblSGDesc.grid(row=2, column=2)
    txtSGDesc = Entry(f1, font=('arial', 10, 'bold'), textvariable=description, bd=5, insertwidth=4, bg="powder blue",
                      justify='right')
    txtSGDesc.grid(row=2, column=3)

    # Show Details
    btnSD = Button(f1, padx=6, pady=6, bd=8, fg="black", font=('arial', 10, 'bold'), width=10, text="Details by SGID",
                   bg="thistle", command=get_sg_details).grid(row=9, column=1)

    # Reset button
    btnReset = Button(f1, padx=6, pady=6, bd=8,
                      fg="black", font=('arial', 10, 'bold'),
                      width=10, text="Reset", bg="thistle",
                      command=reset).grid(row=9, column=2)
    # Show Rules
    btnRules = Button(f1, padx=6, pady=6, bd=8,
                      fg="black", font=('arial', 10, 'bold'),
                      width=10, text="Rules by SGID", bg="thistle",
                      command=get_sg_rules).grid(row=9, column=3)

    # Show matches of SGs
    btnMatchSG = Button(f1, padx=6, pady=6, bd=8,
                        fg="black", font=('arial', 10, 'bold'),
                        width=10, text="SGs by Name", bg="thistle",
                        command=get_sg_by_name).grid(row=9, column=4)
    root.mainloop()


def main():
    app()


if __name__ == "__main__":
    main()

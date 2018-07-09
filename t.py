import json
dic = {"parags":[{"c":"body{\r\nfont-family:Arial,Helvetica,sans-serif;\r\nfont-size:12pt;\r\nmargin:0px auto;\r\nheight:auto;\r\nwidth:800px;\r\nborder:1px solid #006633;\r\n}\r\n#header{\r\nheight:100px;\r\nwidth:800px;\r\nbackground-image:url(plane.jpg);\r\nbackground-repeat:no-repeat;\r\nmargin:0px 0px 3px 0px;\r\n}\r\n#navigator{\r\nheight:25px;\r\nwidth:800px;\r\nfont-size:14px;\r\nlist-style-type:none;\r\n}\r\n#navigator li{\r\nfloat:left;\r\n}\r\n#navigator li a{\r\ncolor:#000000;\r\ntext-decoration:none;\r\npadding-top:4px;\r\ndisplay:block;\r\nwidth:131px;\r\nheight:22px;\r\ntext-align:center;\r\nbackground-color:#009966;\r\nmargin-left:2px;\r\n}\r\n#navigator li a:hover{\r\nbackground-color:#006633;\r\ncolor:#FFFFFF;\r\n}\r\n#content{\r\nheight:auto;\r\nwidth:780px;\r\nline-height:1.5em;\r\npadding:10px;\r\n}\r\n#content p{\r\ntext-indent:2em;\r\n}\r\n#content h3{\r\nfont-size:16px;\r\nmargin:10px;\r\n}\r\n#footer{\r\nheight:50px;\r\nwidth:780px;\r\nline-height:2em;\r\ntext-align:center;\r\nbackground-color:#009966;\r\npadding:10px;\r\n}\r\n*{\r\nmargin:0px;\r\npadding:0px;\r\n}\r\n\r\n","t":"txt"}],"page":1,"tn":1}
print(type(dic))
s = str(dic)
print(type(s))
j = json.loads(s)


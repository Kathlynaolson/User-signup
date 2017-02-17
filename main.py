#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import re

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USERNAME_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_RE.match(password)

EMAIL_RE= re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def build_page(username_input="", email_input="", user_error="", password_error="",verification_error="",email_error=""):

    style = '''
            <head>
            <style type="text/css">
            .label {text-align: right}
            .error {color: red}
            </style>
            </head>
            '''

    username_label= "<td class='label'> Username: </td>"
    username_input= "<td><input type='text' name='username' value=%s></td>" %(username_input)
    error_username= "<td class= 'error'> %s </td>" % (user_error)
    Username= username_label + username_input + error_username

    password_label= "<td class='label'> Password: </td>"
    password_input= "<td><input type='password' name='password'></td>"
    error_password="<td class= 'error'> %s </td>" %(password_error)
    Password= password_label + password_input + error_password

    verify_label= "<td class='label'> Verify: </td>"
    verify_input=  "<td><input type='password' name='password_verify'></td>"
    error_verify="<td class= 'error'> %s </td>" %(verification_error)
    Verification= verify_label + verify_input + error_verify


    email_label= "<td class='label'> Email (Optional): </td>"
    email_input= "<td><input type='text' name='email' value=%s></td>" %(email_input)
    error_email="<td class= 'error'> %s </td>" %(email_error)
    Email= email_label + email_input + error_email

    submit = "<input type='submit'/>"

    form = ("<form  method='post'>" + "<table>" +
              "<tr>" +  Username + "</tr>" +
              "<tr>" + Password + "</tr>" +
              "<tr>" + Verification + "</tr>" +
              "<tr>" + Email + "</tr>" +
              "</table>"  + submit + "</form>")

    header = "<h2>User Signup</h2>"


    return style + header + form

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page()
        self.response.write(content)

    def post(self):
        have_error = False
        username= self.request.get("username")
        password= self.request.get("password")
        verify= self.request.get("password_verify")
        email= self.request.get("email")

        parameters= dict()

        if not valid_username(username):
            parameters['error_username']= "That's not a valid username."
            have_error  = True

        if not valid_password(password):
            parameters['error_password']= "That's not a valid password."
            have_error = True
        elif password != verify:
            parameters['error_verify'] = "Your passwords don't match!"
            have_error = True

        if not valid_email(email):
            parameters['error_email']= "That's not a valid email!"
            have_error = True

        if have_error:
            content = build_page(username,
                                 email,
                                 parameters.get("error_username",""),
                                 parameters.get("error_password",""),
                                 parameters.get("error_verify",""),
                                 parameters.get("error_email",""))
            self.response.write(content)

        else:
            self.redirect('/Welcome?username='+ username)

class Welcome(MainHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("Welcome, "+ username)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', Welcome)
], debug=True)

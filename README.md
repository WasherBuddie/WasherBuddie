# WasherBuddie

## Table of Contents
- [Introduction](#introduction)
- [Admin User Manual for Laundry System](#admin-credentials-and-login)
- [Standard User Manual for Laundry System](#standard-user-manual-for-laundry-system)

## Introduction
WasherBuddie is a smart laundry management system that helps users track their laundry and receive notifications when their laundry cycles are complete. The system supports both washers and dryers, and can notify users via email or text message.

---

### **Admin User Manual for Laundry System**

#### **Admin Credentials and Login**
- Use the provided starter **admin credentials** to log in. Once logged in, click the **menu button** and navigate to **User Preferences** to change your password, email, and other personal settings.

#### **Admin Dashboard**
- After logging in as an **admin**, go to **User Preferences**, where the **Admin Settings** button will be highlighted.
  
  **Admin Functions:**
  - **Add Washers and Dryers**: Use the respective buttons to add washers and dryers to the system.
  - **Set Machines In/Out of Order**: You can mark machines as out of order or in order as needed.
  - **Delete Machines**: Machines can also be deleted from the system.
  - **Manage User Accounts**: Scroll down to the **User Area** to view all user accounts (except your own). You can:
    - **Promote Users to Admin**: Use the respective button to give users admin privileges.
    - **Delete User Accounts**: Use the respective button to delete user accounts.

#### **Send Message to Users**
- Scroll further down to find the **Send Message Box**. This allows you to send messages to all users of the site with any updates or notifications you deem necessary.

#### **Admin Page Navigation**
- The **Admin Page** is accessible without logging in, but none of the functionality will work until you are logged in as an admin.

#### **Home Page Features**
- **View Washers and Dryers**: All washers and dryers are visible on the home page. However, you can only start a session with a machine if you are signed into an account.
- **Machine Sessions**:
  - **Washer Sessions** last for **50 minutes**.
  - **Dryer Sessions** last for **60 minutes** (based on Delta Tau Delta machine settings).
  - Once a session begins, it **cannot be stopped**.
  - When the session ends, the user will receive an **email notification** that their laundry is done, and the machine status will change back to "available."
  
#### **Machine Status**
- If a machine is set **out of order**, no one will be able to use it.

#### **Navigation Tips**
- To return to the **home page**, click the **WasherBuddie logo** located in the top left corner of any page.

#### **Password Recovery**
- If you forget your password, go to the **login screen** and click **Forgot Password**. A **temporary code** will be sent to your email to allow you to log in and reset your password.

#### **Creating a New Account**
- On the **login screen**, there is an option to **create a new account**. Fill in the required fields, and if all credentials are valid, the account will be created. Then, log in with the credentials you just entered.

#### **Logging Out**
- To **log out**, navigate to the top right corner, click the **menu button**, and select **Logout**.

---

### **Standard User Manual for Laundry System**

#### System Requirements
- Web browser with JavaScript enabled
- Valid email address
- Mobile phone number (for text notifications)

#### Creating a New Account
1. Navigate to the registration page by clicking "Create Account"
2. Fill in the required information:
   - Full Name
   - Email Address
   - Phone Number (10 digits)
   - Phone Carrier (for text notifications)
   - Preferred Notification Method (Email or Text)
   - Password
3. Click "Create Account" to complete registration

#### User Account Management

##### Logging In
1. Visit the login page
2. Enter your email address
3. Enter your password
4. Click "Login"

##### Updating User Preferences
1. Navigate to "User Preferences"
2. You can modify:
   - Name
   - Email Address
   - Phone Number
   - Phone Carrier
   - Notification Preference
   - Password
3. Click "Save Changes" to update your information

##### Password Requirements
- Must be a string
- No length restrictions, but strong passwords are recommended

#### Using the Laundry System

##### Viewing Machine Status
From the home page, you can see:
- Available machines
- Machines in use
- Machine status (Available/In Use)
- Time remaining for machines in use

##### Starting a Laundry Session
1. Locate an available machine
2. Click "Start Session" on your chosen machine
3. Load your laundry and start the machine
4. The system will track your session

##### Ending a Laundry Session
1. When your cycle is complete, you'll receive a notification
2. Go to the laundry room and remove your items
3. Click "End Session" in the app
4. The machine will become available for other users

#### Notifications

##### Notification Types

###### Email Notifications 
Include:
- Greeting with your name
- Machine type (Washer/Dryer)
- Completion message
- Request to collect laundry
- WasherBuddie signature

###### Text Notifications 
Include:
- Machine type
- Completion message
- Brief instructions
- WasherBuddie signature

#### Notification Settings
1. Go to "User Preferences"
2. Choose your preferred notification method:
   - Email
   - Text
3. Ensure your contact information is correct
4. Save your changes
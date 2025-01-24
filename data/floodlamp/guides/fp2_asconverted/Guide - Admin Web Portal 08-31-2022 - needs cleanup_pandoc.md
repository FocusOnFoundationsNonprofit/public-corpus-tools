# 

# **Admin Web Portal Guide**

[Overview](#overview)

[All Roles - Brief Description](#all-roles---brief-description)

# 

# [Admin - Main Tasks](#admin---main-tasks-1)

[<u>Login</u>](#login)

[<u>Adding other Users and Granting Staff or Admin roles</u>](#login)

[<u>Adding users with csv “Import Users” function</u>](#adding-users-with-csv-import-users-function)

[<u>Monitoring Onboarding</u>](#monitoring-onboarding)

[<u>Using Kits and Tubes views</u>](#using-kits-and-tubes-views)

[<u>Triggering password reset links</u>](#cfpmgngp78nj)

[<u>Exporting csv of results</u>](#exporting-csv-of-results)

# 

# [Admin - Troubleshooting](#admin---troubleshooting-1)

[<u>Troubleshoot tubes that does not intake (“No such barcode exists” error message)</u>](#troubleshoot-tubes-that-do-not-intake-no-such-barcode-exists-error-message)

[<u>Troubleshoot user that can’t be added at collection step</u>](#troubleshoot-user-that-cant-be-added-at-collection-step)

# 

# [Admin - Advanced](#admin---advanced-1)

[<u>Changing Consent (must get written approval from FloodLAMP)</u>](#changing-consent-must-get-written-approval-from-floodlamp)

[<u>Adding a new participant group</u>](#adding-a-new-participant-group)

# Overview

The FloodLAMP Mobile App and Admin Web Portal are a system that manages pooled surveillance testing, including:

-   participant onboarding, as individuals and households;

-   electronic consent signing;

-   self-directed pooled sample collection and accessioning;

-   tracking, processing, and resulting sample tubes;

-   participation and results monitoring.

There are 3 main roles for users of the system and corresponding views of the app and portal.

## Participants - people submitting samples for testing.

The Participant View of the FloodLAMP Mobile App is used for:

-   updating profile information such as name, email, and phone number;

-   adding minors under a guardian’s account;

-   registering pooled sample collections by listing the names of who is contributing samples;

-   checking the status of previously collected sample tubes.

All users of the system typically have the privileges of the Participant role (able to be added to a collection) whether or not they actually have the role included.

## Staff - people processing samples (i.e. running the actual test in the lab)

The Staff View of the FloodLAMP Mobile App is used for:

-   intaking collected tubes by scanning their QR codes;

-   batching tubes together for processing;

-   updating the status tubes at various points of processing (optional);

-   entering test results (positive, negative, inconclusive, invalid).

Users who have been granted the Staff role should also be granted the AccessStaff role as well, and the term “Staff” usually refers to the users with both roles. These Staff can access the Staff View where they process tubes without access to Personal Identifiable Information (PII). Staff will require moderate training.

## Admin - program managers

The Admin Web Portal is only available via desktop/laptop browser and not through the FloodLAMP Mobile App, though both are accessing the same database of information. It is used for:

-   managing the entire testing program;

-   overseeing the onboarding process;

-   adding users and granting roles;

-   customizing messages and information;

-   viewing the status of tubes and participants;

-   reviewing results and participation history.

The FloodLAMP Mobile App runs on the Appivo Platform and typically, admin privileges should be granted in each. The “Admin” role is granted within the FloodLAMP Mobile App (under “My Apps” in the Appivo Platform) and gives access to the Admin Web Portal. “System Administrator” is granted in the Appivo Platform and enables granting roles both within the App and Appivo Platform (see above [<u>Adding Users and Granting Staff and Admin Roles</u>](#adding-users-and-granting-staff-or-admin-roles)).

#  

# All Roles - Brief Description

**Participant** can be added to collections, only needed if user has no other roles

**Sponsor** can perform collections with approval (ignore if using SuperSponsor for all)

**SuperSponsor** can perform collections on anyone, i.e. see everyone in their group when adding to collection

**Staff** can use the Staff View to process tubes

**AccessStaff** add together with Staff role, used for “Access Groups” of Staff to link to Groups (participants)

**PI** special role that receives email and text notifications with PII for Positive and Inconclusive results

**Administrator** can view and utilize the Admin Web Portal

**System Administrator** (Appivo platform role) can change user roles from the Appivo User view in top right

# 

# Admin - Main Tasks

## Login 

Log in at [<u>https://apps.appivo.com/</u>](https://apps.appivo.com/) - your account must have been granted the “Admin” role by a System Administrator in order to view the Admin Web Portal.<img src="media/image8.png" style="width:1.25582in;height:1.51982in" />

## 

## Adding Users and Granting Staff or Admin roles

Go to the Appivo User view (in top right corner under the head circle icon)

-   pencil edit icon edits user profile info<img src="media/image4.png" style="width:7in;height:2.05556in" />

<img src="media/image7.png" style="width:1.94271in;height:2.49448in" />

-   this is also where you can trigger a Password Reset to be sent to the user (<span id="cfpmgngp78nj" class="anchor"></span>**Triggering password reset links)**

<!-- -->

-   clicking the user name or anywhere in the line opens up the view to edit their roles

<img src="media/image3.png" style="width:6.79688in;height:2.23528in" />

Example Admin:

<img src="media/image6.png" style="width:6.37441in;height:2.57033in" />

Example Staff:

<img src="media/image10.png" style="width:2.45713in;height:2.31651in" />

To get back to the Admin Web Portal:

1.  click “My Apps” from top right menu bar

2.  click the “FloodLAMP” logo on the left side

## <img src="media/image2.png" style="width:7in;height:2.58333in" />

## Adding users with csv “Import Users” function

Specify role - typically SuperSponsor which includes Participant role privileges)

WIP

## 

## 

## Monitoring Onboarding

From the Users tab, you can check if folks who have signed up through the form or had their accounts created (import or manual) have actually clicked through to set their password, signed into the app (where they are prompted right away to sign the consent), and have added minors.

## <img src="media/image9.png" style="width:7in;height:3.33333in" /> 

## Using Kits and Tubes views

These tabs are used to check the status or result of a tube or participant who added to a collection.

It’s also used to review tubes collected that day and who is in them.

“Kits” shows a view where each line is an individual QR coded tube - which could contain a single sample from an individual or from several people in a pool.

“Tubes” shows a view where each line is a Participant, but this is sorted by the Tube ID so you will see the people in a pool listed together.

Apologies to the mixed up terminology - these will be changed shortly.

<u>Tubes Tab</u>

The Tubes tab shows the results of a screening session. This can be used or to track down a Participant or their sample tube. Each row of the table on this tab represents a unique collection event (i.e., Tube ID + Participant or Tube ID + Minor). The Tubes tab allows you to:

-   Find Participants & Minors within a positive pool

-   View timestamp of Staff collection and results

-   See notes added by the Sponsor

-   Search by name or Tube ID

-   Export all data or a date-limited set of data

## <img src="media/image11.png" style="width:6.89063in;height:4.0352in" />

## 

## 

## 

## 

## 

## 

## 

## 

## 

<u>Kits Tab</u>

<img src="media/image5.png" style="width:7.35763in;height:3.05309in" />

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## Exporting csv of results

Available from either the Kits or the Tubes tab.

# 

# 

# Admin - Troubleshooting

## Troubleshoot tubes that do not intake (“No such barcode exists” error message)

-   This is usually because a participant forgot to complete the collect step (on Participant view of App).

-   Can also be caused by the barcode/QRcode being manually typed in and being incorrect (such as having a trailing whitespace character).

## Troubleshoot user that can’t be added at collection step

-   If Minor, it’s likely because they are not searching the Guardian name first. Minors are nested underneath the Guardian user that added them.

-   May be due to the email for the Participant user being entered incorrectly.

-   May be due to the Participant user not being included in the group.

# Admin - Advanced

## Changing Consent (must get written approval from FloodLAMP)

WIP

## 

## Adding a new participant group

WIP

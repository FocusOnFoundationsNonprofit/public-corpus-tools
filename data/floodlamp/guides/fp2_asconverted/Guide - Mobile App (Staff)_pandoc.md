# Overview

The app is used to guide the lab workflow, track the status of collected tubes, and notify the program admin and participants of the completion of the test. The basic steps for the workflow are:

1.  **Intake** – log tubes for processing

2.  **Process** – update status of tubes during the run/set to amp

3.  **Result** – update status of tubes and notify program admin and participants

# Staff App Training

## Accessing the Staff Side 

With an account that has staff privileges (“Staff” and “AccessStaff” roles),, one can change to the Staff Role/View by tapping on the hamburger menu ( ☰ ) in the top left corner.

<img src="media/image4.png" style="width:7in;height:4.80556in" />

## **Intake Tubes**

The Intake step changes the status of tubes from “Collected” to “Received”. Only tubes where the Collection step is completed by the Sponsor will be recognized at the Intake step. Intake can happen before inactivation or while waiting for amplification. Staff can intake tubes into Batches that can be progressed through the system together. Batches are automatically assigned a date-based ID, though you can choose any unique name.

1.  Tap the INTAKE Button

2.  Chose batch action option

    -   NO BATCH: Intake tube individually

    -   CREATE BATCH: Create a new Batch

    -   ADD TO BATCH: Add the tube to an existing batch

3.  Select "CREATE BATCH" and name the new batch or approve the default name<img src="media/image6.png" style="width:6.32578in;height:3.32292in" />

4.  Scan tubes to add to the batch, or enter the barcode manually (tap “Cancel” to exit the scanner)

5.  Click the **&lt;** button at the top left to return to the home screen <img src="media/image2.png" style="width:4.21354in;height:3.20405in" />

## Process Tubes 

The Process view allows staff to update the status of batches or tubes in the run.

-   Tap the PROCESS button on the home page

-   Select the batch or tube (tap the circle to the left) and tap the check button at the bottom of the screen<img src="media/image7.png" style="width:7in;height:3.56944in" />

Update the status of a batch or tube by selecting an option and tapping "Update status"

-   “RECEIVED” is the status after the Intake step

-   “INACTIVE” is the inactivation step

-   “AMP” is the amplification step – selecting this status moves batches and tubes to the "RESULTS" view

If only processing a single batch of tubes, it’s advised to skip updating the batch for the inactivation stage. You may update to AMP as soon as the samples are on the amplification heater. After doing so, you’ll no longer see the batch in the process screen. Tap the (＜) in the top left to return to the main staff view.<img src="media/image8.png" style="width:5.2958in;height:3.63316in" />

## Resulting Tubes

At this stage, you have completed running the physical test, and you know the result for every pool. The Result you input into the App is the final result, after any reruns if done (i.e. the final “call”). In most batches, all tubes will be negative. In the instances where this is not the case, you must pull the non-negative tubes out of the batch so that they can be resulted separately.

To pull out a tube from a batch: (see video [<u>App Staff - Pulling tube out of batch</u>](https://vimeo.com/745913329/4239dafd1c))

1.  Tap the right arrow icon (➔) on the right end of the row

2.  Search for the tube(s) with the non-negative result(s)

3.  Press the small red “✕” on the right end of the row to remove the tube from the batch

4.  The tube(s) should now appear in the section below the list of batches in the results screen and can be resulted individually<img src="media/image3.png" style="width:6.06771in;height:3.35891in" />

Tubes or batches marked as "AMP" in the Process step are visible in the Results view

1.  Tap RESULTS on home screen

2.  Select the desired tubes or batches to modify and tap UPDATE at the bottom left of the screen

3.  Tap RESULT in the pop-up screen to update the status of the tube or batch. Result options will appear:

    1.  NULL – no value (this is the default)

    2.  INVALID – If the negative or positive controls do not produce negative and positive results, respectively, then the remaining results cannot be interpreted and the run is considered invalid

    3.  INCONCLUSIVE – test result is neither clearly positive or negative, beyond the edge case colors

    4.  NEGATIVE – a negative result

    5.  POSITIVE – a positive result

**Note:** Marking a tube as positive notifies all listed PIs in the tenant of the result.

Select the result and tap “Update Status.”

1.  On the Result screen, select the desired tubes or batches and tap NOTIFY, then OK if you wish to continue.

    1.  This moves the tube to history and changes participant and sponsor tube status to “completed”.

    2.  *Note: Notifications to Participants are currently turned off globally in the FloodLAMP Mobile App to comply with non-diagnostic surveillance testing guidance.*

<img src="media/image5.png" style="width:7in;height:3.86111in" />

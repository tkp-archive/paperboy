Paperboy UI Design 

* Why?
* Paperboy needs to allow users easily upload notebooks however they so choose, and parameterize and schedule notebooks. After doing so, the user should get timely reports generating the data intended by the notebooks. At the same time, Paperboy should be a library for notebooks/jobs/reports that are marked as “public” by users to be shared in the Paperboy community. IN other words, it will maintain the open source spirit it was built in.
* Goal: “ As an analyst/data scientist, I want to schedule notebooks and run jobs to create reports that will generate time-sensitive data in an effective and routinely manner.

* User Journey:
1. The journey begins with a new user. Ideally, the user would be able to access a Paperboy account using o-auth. This o-auth can be “Login using Google,” Login using Facebook,” or some authorization domain. The user should rarely see the login screen. 
* 1. 5 If the login screen appears, the user creates an account, taking the user to a page that requests a username, email, password, and password confirmation. The user then selects “Create Account” to be able to log in. 
2. User arrives at Home Screen, which would show the most recent report for a seasoned user, but since the user has not used Paperboy before, the user selects “Help” at the top of the website to read documentation on how to use Paperboy. By default, the screen timeout is one hour.
3. The user then adds a first notebook to the application, parameterizes the notebook, and finally schedules a job. The job will take said parameters and produce a report.
4. The user will receive the desired report as a result of the notebook’s code and parameterizations.
5. Given that reports are not made instantaneously, the user can go to the status page to check on the progress of jobs and reports.
6. After gaining familiarity with the functionality of Paperboy, the user can change settings such as notifications for when a report is finished or has failed to be completed, and the theme of the website. Additionally, the user can change the associated email address, password, and screen timeout limit.
7. After accumulating a large volume of notebooks, reports, and jobs, the user can switch between icon and detailed views of these files for easier access or identification. This option is available from the start, but becomes more necessary once a lot of files are accumulated. 
8. To filter through so many files, the user can mark particular ones as favorites, and choose to look at favorites to quickly access preferred files.
9. Since Paperboy is a library, the user can use the search bar to find public notebooks, jobs, and reports. The user can save a copy of them to the personal account and modify them at will.
10. Once a user is done using Paperboy, the user can select to log out and will be returned to the home screen. If the user no longer wants a Paperboy account, the user can select under the username to delete an account and go back to the login screen.

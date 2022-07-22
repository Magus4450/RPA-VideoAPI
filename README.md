## How to run

1. Make a virtual environment <br>
`python3 -m venv env`


2. Activate virtual envrionment <br>
`source /env/Scripts/activate` for Win <br>
`bin /env/lib/activate` for Mac / Linux


3. Install requirements <br>
`pip install -r requirements.txt`

4. Migrate <br>
`python3 manage.py migrate`

5. Run <br>
`python3 manage.py runserver`


<hr>

## API Endpoints

#### 1.  `/api/video/create/`
*Upload a new video*
<ul>
    <li> Allowed Requests: <strong>POST</strong> </li>
    <li> Payloads</li>
        <ul>
            <li> video : file</li>
        </ul>
    <li> Constraints: </li>
        <ul>
            <li> File type should be either .mp4 or .mkv</li>
            <li> File size should be less then 1GB </li>
            <li> Video length should be less than 10 minutes </li>
        </ul>

</ul>


#### 2.  `/api/video/uploading/`
*Get list of videos being currently uploaded*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>

</ul>


#### 3.  `/api/video/charges<int:size_bytes>/<int:length_seconds>/<str:video_type>/`
*Get charge of video of given parametes*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>

</ul>

#### 4.  `/api/video/size/<int:minm>/<int:maxm>/`
*Get list of videos of size in given range*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>

</ul>

#### 5.  `/api/video/date/<str:date>/`
*Get list of videos published after given date*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>

</ul>

#### 6.  `/api/video/length/<int:minm>/<int:maxm>/`
*Get list of videos of length in given range*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>

</ul>

#### 7.  `/api/video/all/`
*Get list of all videos*
<ul>
    <li> Allowed Requests: <strong>GET</strong> </li>
</ul>





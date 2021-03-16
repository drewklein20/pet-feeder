<?php
header('Access-Control-Allow-Origin: *');
cors();
/*
Drew Klein - Dog feeder
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

$dbhost = 'localhost';
$dbuser = 'remote';
$dbpass = 'PetFeeder2021!';
$dbname = 'Feeder';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    //------------------------------------------------
    //-------------- POST REQUESTS -------------------

    $action           = isset($_POST["action"]) ? clean_input($_POST["action"]) : '';
    $username         = isset($_POST["username"]) ? clean_input($_POST["username"]) : '';
    $password         = isset($_POST["password"]) ? clean_input($_POST["password"]) : '';
    $feedTime         = isset($_POST["feed_time"]) ? clean_input($_POST["feed_time"]) : '';
    $amount           = isset($_POST["amount"]) ? clean_input($_POST["amount"]) : '';
    $id               = isset($_POST["id"]) ? clean_input($_POST["id"]) : '';
    $preferences      = isset($_POST["preferences"]) ? getJSONbody($_POST["preferences"]) : null;
    $rc = false;

    switch ($action) {
        case 'auth':
            $sql = "SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.username')) as username, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.password')) as password FROM Feeder.Settings limit 1;";
            $results = queryDB($sql);
            $authU = $results[0]['username'];
            $authP = $results[0]['password'];

            if ($username == $authU && $password == $authP) {
                echo 'true';
            } else {
                echo 'false';
            }
            break;
        case 'feed_now':
            $sql = "INSERT INTO `Feeder`.`Logs` (`amount`, `trigger`) VALUES ('" . $amount . "', 'app')";
            $rc = execQuery($sql);
            if ($rc) {
                $command = 'sudo python /var/www/html/php/feed.py';
                exec($command, $out, $status);
                echo "Done!";
            } else {
                echo "There was an error dispensing the food..";
            }
            break;
        case 'add_schedule':
            $sql = "INSERT INTO `Feeder`.`Schedule` (`feedTime`, `amount`) VALUES ('" . $feedTime . "', '" . $amount . "')";
            $rc = execQuery($sql);
            if ($rc) {
                echo "Adding scheduled feed.";
            } else {
                echo "There was an error dispensing the food..";
            }
            break;
        case 'delete_schedule':
            $sql = "DELETE FROM `Feeder`.`Schedule` WHERE (`id` = '" . $id . "')";
            $rc = execQuery($sql);
            if ($rc) {
                echo "Removed scheduled feed";
            } else {
                echo "There was an error dispensing the food..";
            }
            break;
        case 'update_preferences':
            $sql = "UPDATE `Feeder`.`Settings` SET `preferences` = '" . $preferences . "'";
            $rc = execQuery($sql);
            if ($rc) {
                echo "Settings updated.";
            } else {
                echo "There was an error updating settings..";
            }
            break;
        case 'reset_scale':
            $command = 'sudo systemctl restart scale.service';
            exec($command, $out, $status);
            echo "Done!";
            break;
        case 'reset_alexa':
            $command = 'sudo systemctl restart alexa.service';
            exec($command, $out, $status);
            echo "Done!";
            break;
        default:
            echo $action . " not allowed";
            break;
    }
} else if ($_SERVER["REQUEST_METHOD"] == "GET") {
    //------------------------------------------------
    //-------------- GET REQUESTS -------------------

    $action      = isset($_GET["action"]) ? clean_input($_GET["action"]) : '';
    $id          = isset($_GET["id"]) ? clean_input($_GET["id"]) : '';
    $interval    = isset($_GET["interval"]) ? clean_input($_GET["interval"]) : '';
    $timeUnit    = isset($_GET["timeUnit"]) ? clean_input($_GET["timeUnit"]) : '';

    switch ($action) {
        case 'feed_logs':
            $sql = "SELECT * FROM Logs ORDER BY timestamp desc;";
            $results = queryDB($sql);
            $results = str_replace("u2019", "’", $results);
            echo json_encode($results);

            break;
        case 'feed_schedule':
            $sql = "SELECT * FROM Schedule ORDER BY feedTime asc;";
            $results = queryDB($sql);
            echo json_encode($results);

            break;
        case 'current_weight':
            $sql = "SELECT * FROM Weights ORDER BY timestamp desc limit 1;";
            $results = queryDB($sql);
            echo json_encode($results);

            break;
        case 'all_weights':
            $sql = "SELECT * FROM Weights WHERE timestamp > date_sub(now(), interval " . $interval . " " . $timeUnit . ")  ORDER BY timestamp asc;";
            $results = queryDB($sql);
            echo json_encode($results);

            break;
        case 'feeder_settings':
            $sql = "SELECT preferences FROM Settings WHERE id = '" . $id . "';";
            $results = queryDB($sql);
            echo json_encode($results);

            break;
        default:
            echo $action . " not allowed";
            break;
    }
} else {
    echo "No data posted with HTTP REQUEST.";
}

function queryDB($sql)
{
    $dbhost = 'localhost';
    $dbuser = 'remote';
    $dbpass = 'PetFeeder2021!';
    $dbname = 'Feeder';
    $dblink = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

    // Check connection was successful
    if ($dblink->connect_errno) {
        printf("Failed to connect to database");
        exit();
    }

    // Execute query
    $result = $dblink->query($sql);

    // Initialize array variable
    $dbdata = array();

    // Fetch into associative array
    while ($row = $result->fetch_assoc()) {
        $dbdata[] = $row;
    }

    $dblink->close();

    return $dbdata;
}


function execQuery($sql)
{
    $rc = false;
    $dbhost = 'localhost';
    $dbuser = 'remote';
    $dbpass = 'PetFeeder2021!';
    $dbname = 'Feeder';
    // Used when we don't need to do something with the result besides see if it was successful
    $dblink = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

    // Check connection was successful
    if ($dblink->connect_errno) {
        printf("Failed to connect to database");
        exit();
    }

    // Execute query
    if ($dblink->query($sql) === TRUE) {
        $rc = true;
    } else {
        $rc = false;
        echo "Error: " . $sql . "<br>" . $dblink->error;
    }

    $dblink->close();

    return $rc;
}

function clean_input($data)
{
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

function clean_html($value)
{
    $search = array("\\",  "\x00", "\n",  "\r",  "'",  '"', "\x1a");
    $replace = array("\\\\", "\\0", "\\n", "\\r", "\'", '\"', "\\Z");

    return str_replace($search, $replace, $value);
}

function cleanSingleField($data)
{
    $data = trim($data);
    $data = htmlspecialchars($data);
    return $data;
}

function getJSONbody($data)
{
    $data = trim($data);
    $data = htmlspecialchars($data);
    $data = stripslashes($data);
    $data = str_replace('&quot;', '"', $data);
    $data = str_replace('\'', '?', $data);
    $data = str_replace(', }', '}', $data);

    return $data;
}

function jsonFixer($json)
{
    $patterns     = [];
    /** garbage removal */
    $patterns[0]  = "/([\s:,\{}\[\]])\s*'([^:,\{}\[\]]*)'\s*([\s:,\{}\[\]])/"; //Find any character except colons, commas, curly and square brackets surrounded or not by spaces preceded and followed by spaces, colons, commas, curly or square brackets...
    $patterns[1]  = '/([^\s:,\{}\[\]]*)\{([^\s:,\{}\[\]]*)/'; //Find any left curly brackets surrounded or not by one or more of any character except spaces, colons, commas, curly and square brackets...
    $patterns[2]  =  "/([^\s:,\{}\[\]]+)}/"; //Find any right curly brackets preceded by one or more of any character except spaces, colons, commas, curly and square brackets...
    $patterns[3]  = "/(}),\s*/"; //JSON.parse() doesn't allow trailing commas
    /** reformatting */
    $patterns[4]  = '/([^\s:,\{}\[\]]+\s*)*[^\s:,\{}\[\]]+/'; //Find or not one or more of any character except spaces, colons, commas, curly and square brackets followed by one or more of any character except spaces, colons, commas, curly and square brackets...
    $patterns[5]  = '/["\']+([^"\':,\{}\[\]]*)["\']+/'; //Find one or more of quotation marks or/and apostrophes surrounding any character except colons, commas, curly and square brackets...
    $patterns[6]  = '/(")([^\s:,\{}\[\]]+)(")(\s+([^\s:,\{}\[\]]+))/'; //Find or not one or more of any character except spaces, colons, commas, curly and square brackets surrounded by quotation marks followed by one or more spaces and  one or more of any character except spaces, colons, commas, curly and square brackets...
    $patterns[7]  = "/(')([^\s:,\{}\[\]]+)(')(\s+([^\s:,\{}\[\]]+))/"; //Find or not one or more of any character except spaces, colons, commas, curly and square brackets surrounded by apostrophes followed by one or more spaces and  one or more of any character except spaces, colons, commas, curly and square brackets...
    $patterns[8]  = '/(})(")/'; //Find any right curly brackets followed by quotation marks...
    $patterns[9]  = '/,\s+(})/'; //Find any comma followed by one or more spaces and a right curly bracket...
    $patterns[10] = '/\s+/'; //Find one or more spaces...
    $patterns[11] = '/^\s+/'; //Find one or more spaces at start of string...

    $replacements     = [];
    /** garbage removal */
    $replacements[0]  = '$1 "$2" $3'; //...and put quotation marks surrounded by spaces between them;
    $replacements[1]  = '$1 { $2'; //...and put spaces between them;
    $replacements[2]  = '$1 }'; //...and put a space between them;
    $replacements[3]  = '$1'; //...so, remove trailing commas of any right curly brackets;
    /** reformatting */
    $replacements[4]  = '"$0"'; //...and put quotation marks surrounding them;
    $replacements[5]  = '"$1"'; //...and replace by single quotation marks;
    $replacements[6]  = '\\$1$2\\$3$4'; //...and add back slashes to its quotation marks;
    $replacements[7]  = '\\$1$2\\$3$4'; //...and add back slashes to its apostrophes;
    $replacements[8]  = '$1, $2'; //...and put a comma followed by a space character between them;
    $replacements[9]  = ' $1'; //...and replace by a space followed by a right curly bracket;
    $replacements[10] = ' '; //...and replace by one space;
    $replacements[11] = ''; //...and remove it.

    $result = preg_replace($patterns, $replacements, $json);

    return $result;
}

function cors()
{

    // Allow from any origin
    if (isset($_SERVER['HTTP_ORIGIN'])) {
        // Decide if the origin in $_SERVER['HTTP_ORIGIN'] is one
        // you want to allow, and if so:
        header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Max-Age: 86400');    // cache for 1 day
    }

    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            // may also be using PUT, PATCH, HEAD etc
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

        exit(0);
    }
}

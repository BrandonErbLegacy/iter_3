<?php
//Purpose of this file is to be the logical storage driver between
//The client/server

function connect(){
  $servername = "localhost";
  $username = "id3837140_mcuser";
  $password = "mcpassword";
  $db = "id3837140_mctest";
  // Create connection
  $conn = new mysqli($servername, $username, $password, $db);
  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  }
  return $conn;
}

function getSaveStamp($categoryName){
  $sql = "SELECT * FROM Categories WHERE Name = '$categoryName'";
  $conn = connect();
  if ($conn->connect_error){
    die('Error: ' . mysqli_error($conn));
  }
  $CAT = $conn->query($sql);
  $CAT_ID = $CAT->fetch_assoc()["SaveStamp"];
  echo(json_encode($CAT_ID));
}
function discoverScriptsByCategory($categoryName){
 //Retrieve CategoryUID, find scripts via relation, and retrieveScript()
 $sql = "SELECT * FROM Categories WHERE Name = '$categoryName'";
 $conn = connect();
 if ($conn->connect_error){
   die('Error: ' . mysqli_error($conn));
 }
 $CAT = $conn->query($sql);
 $CAT_ID = $CAT->fetch_assoc()["UID"];
 //echo($CAT_ID);
 $sql = "SELECT * FROM CategoryScriptRelation WHERE CategoryUID = '$CAT_ID'";
 $SCRIPT_CATS = $conn->query($sql);
 while ($row = $SCRIPT_CATS->fetch_assoc()) {
   $id = $row['ScriptUID'];
   $sql = "SELECT * FROM Scripts WHERE UID = '$id'";
   $SCRIPT = $conn->query($sql);
   $SCRIPT = $SCRIPT->fetch_assoc();
   echo(json_encode($SCRIPT));
   echo("<br/>");
 }
}
function createScript($scriptUID, $scriptName, $scriptContents, $scriptTargetName){
  $sql = "INSERT INTO Scripts (UID, Contents, Name, TargetName) VALUES ('$scriptUID', '$scriptName', '$scriptContents', '$scriptTargetName')";
  $conn = connect();
  if (!mysqli_query($conn, $sql)){
    die('Error: ' . mysqli_error($conn));
  }
}
function createScriptCatRelation($scriptUID, $catUID){
  $sql = "INSERT INTO CategoryScriptRelation (CategoryUID, ScriptUID) VALUES ('$scriptUID', '$catUID')";
  $conn = connect();
  if (!mysqli_query($conn, $sql)){
    die('Error: ' . mysqli_error($conn));
  }
}
function createCategory($categoryUID, $name, $saveStamp){
  $sql = "INSERT INTO Categories (UID, Name, SaveStamp) VALUES ('$categoryUID', '$name', ''$saveStamp')";
  $conn = connect();
  if (!mysqli_query($conn, $sql)){
    die('Error: ' . mysqli_error($conn));
  }
}
function updateScript($scriptUID, $scriptName, $scriptContents, $scriptTargetName, $saveID){
  $sql = "UPDATE Scripts SET Contents='$scriptContents', Name='$scriptName', TargetName='$scriptTargetName' WHERE UID='$scriptUID'";
  $conn = connect();
  if ($conn->connect_error){
    die('Error: ' . mysqli_error($conn));
  }
  $conn->query($sql);
  $sql = "SELECT * FROM CategoryScriptRelation WHERE ScriptUID = '$scriptUID'";
  $result = $conn->query($sql);
  $catID = $result->fetch_assoc()["CategoryUID"];
  echo($catID);
  $sql = "UPDATE Categories SET SaveStamp='$saveID' WHERE UID='$catID'";
  $conn->query($sql);
}


if (!isset($_POST["action"])){
  echo("Cannot process command.");
} else {
  if ($_POST["AUTH_ID"] == "eca44780-8303-41e1-b12a-a2ae300d7590"){
    switch ($_POST["action"]){
      case "GET_SAVE_STAMP":
        getSaveStamp($_POST["cat_name"]);
        break;
      case "GET_CAT_RELATIONS":
        discoverScriptsByCategory($_POST["cat_name"]);
        break;
      case "CREATE_SCRIPT":
        createScript($_POST["scriptUID"], $_POST["scriptName"], $_POST["scriptContents"], $_POST["scriptTargetName"]);
        break;
      case "UPDATE_SCRIPT":
        updateScript($_POST["scriptUID"], $_POST["scriptName"], $_POST["scriptContents"], $_POST["scriptTargetName"], $_POST["saveID"]);
        break;
      case "RELATE":
        createScriptCatRelation($_POST["categoryUID"], $_POST["name"], $_POST["saveStamp"]);
        break;
    };
  } else {
    echo("Failed authentication");
  }
}
?>

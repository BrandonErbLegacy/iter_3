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



function retrieveScript($scriptID){

}
function discoverScriptsByCategory($categoryName){
 //Retrieve CategoryUID, find scripts via relation, and retrieveScript()
}

function createScript($scriptUID, $scriptName, $scriptContents, $scriptTargetName){
  $sql = "INSERT INTO Scripts (UID, Contents, Name, TargetName) VALUES ('$scriptUID', '$scriptName', '$scriptContents', '$scriptTargetName')";
  $conn = connect();
  if (!mysqli_query($conn, $sql)){
    die('Error: ' . mysqli_error($conn));
  }
}

function createScriptCatRelation($scriptUID, $catUID){

}





if (!isset($_GET["action"])){
  echo("Cannot process command.");
} else {
  switch ($_GET["action"]){
    case "GET":
    case "UPDATE":
      createScript($_GET["scriptUID"], $_GET["scriptName"], $_GET["scriptContents"], $_GET["scriptTargetName"]);
      break;
    case "RELATE":
      echo("Tested!");
      break;
  };
}
?>

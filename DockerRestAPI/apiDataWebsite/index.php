<html>
    <head>
        <title>Brevet calculator REST-api demo: Data lists </title>
    </head>
    <body>
        <!-- Open times -->
        <h1>List of open times </h1>
        <h3> DB-Format: /listOpenOnly/ </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly/');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> JSON-Format: /listOpenOnly/json </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly/json');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> JSON-Format top k times (demo): /listOpenOnly/json?top=3 </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly/json?top=3');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> CSV-Format: /listOpenOnly/csv </h3>
        <ul>
            <?php
            $csv = file_get_contents('http://api-service/listOpenOnly/csv');
            $obj = str_getcsv($csv);
            foreach ($obj as $csv_time_value) {
                echo "<li>$csv_time_value</li>";
            }
            ?>
        </ul>
        </ul>
        <h3> CSV-Format top k times (demo): /listOpenOnly/csv?top=3 </h3>
        <ul>
            <?php
            $csv = file_get_contents('http://api-service/listOpenOnly/csv?top=3');
            $obj = str_getcsv($csv);
            foreach ($obj as $csv_time_value) {
                echo "<li>$csv_time_value</li>";
            }
            ?>
        </ul>


        <!-- Close times -->
        <h1>List of close times </h1>
        <h3> DB-Format: /listCloseOnly/ </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listCloseOnly/');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> JSON-Format: /listCloseOnly/json </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listCloseOnly/json');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        </ul>
        <h3> JSON-Format top k times (demo): /listCloseOnly/json?top=3 </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listCloseOnly/json?top=3');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> CSV-Format: /listCloseOnly/csv </h3>
        <ul>
            <?php
            $csv = file_get_contents('http://api-service/listCloseOnly/csv');
            $obj = str_getcsv($csv);
            foreach ($obj as $csv_time_value) {
                echo "<li>$csv_time_value</li>";
            }
            ?>
        </ul>
        <h3> CSV-Format top k times (demo): /listCloseOnly/csv?top=3 </h3>
        <ul>
            <?php
            $csv = file_get_contents('http://api-service/listCloseOnly/csv?top=3');
            $obj = str_getcsv($csv);
            foreach ($obj as $csv_time_value) {
                echo "<li>$csv_time_value</li>";
            }
            ?>
        </ul>


        <!-- All times -->
        <h1>List of all times </h1>
        <h3> DB-Format: /listAll/ </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> JSON-Format: /listAll/json </h3>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/json');
            $obj = json_decode($json);
            foreach ($obj as $array) {
              foreach($array as $time)
                echo "<li>$time</li>";
            }
            ?>
        </ul>
        <h3> CSV-Format: /listAll/csv </h3>
        <ul>
            <?php
            $csv = file_get_contents('http://api-service/listAll/csv');
            $obj = str_getcsv($csv);
            foreach ($obj as $csv_time_value) {
                echo "<li>$csv_time_value</li>";
            }
            ?>
        </ul>
    </body>
</html>

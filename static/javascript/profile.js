<script type="text/javascript">
        var $SCRIPT_ROOT = { request.script_root|tojson|safe };
    
        var intervalID = setInterval(update_values,5000);
    
            function update_values() {
                $.getJSON($SCRIPT_ROOT + '/profile_data',
                
                    function(data) {
                        $('#f_name').text(data.f_name);
                        console.log(data.f_name);
                    };
                    function(data) {
                        $('#l_name').text(data.l_name);
                        console.log(data.l_name);
                    };
                    function(data) {
                        $('#Id').text(data.Id);
                        console.log(data.Id);
                    })};
    </script>
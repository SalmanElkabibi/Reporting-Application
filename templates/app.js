document.addEventListener('DOMContentLoaded', function() {
    var hideboxes = document.querySelectorAll('input[type=checkbox][name=box]');
    vals = []  
        for (var hidebox of hideboxes)
        {
            hidebox.addEventListener('change', function(event)
            {   
                if (event.target.checked) {
                    vals[0] = event.target.value
                    console.log(vals)           
                }
            });
            
        }
        
    }, false);
    document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[type=checkbox][name=checkbox]');
    tasks = []
        for (var checkbox of checkboxes)
        {
            checkbox.addEventListener('change', function(event)
            {   
                if (event.target.checked) {
                    tasks.push(`${event.target.value}`)
                    console.log(tasks)
                    document.getElementById('tasks').innerHTML = '<div> Order : '+tasks.join("    -    ")+' </div>  <input type="text" name="tasks" class="form-control" value = '+tasks+' id="tasks"  hidden> <br>'
                }
                else {
                    tasks = tasks.filter((task)=>(task !== event.target.value))
                    console.log(tasks)
                    document.getElementById('tasks').innerHTML = '<div> Order : '+tasks.join("    -    ")+' </div>  <input type="text" name="tasks" class="form-control" value = '+tasks+' id="tasks"  hidden> <br>'
                }
            });
            
        }
        
    }, false);
    document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[id=inlineCheckbox7]');
        for (var checkbox of checkboxes)
        {
            checkbox.addEventListener('change', function(event)
            {   
                if (event.target.checked) {
                    document.getElementById('reply_msg').innerHTML = '<label for="reply_msg"><strong>Reply Message</strong></label> <input type="text" name="reply_msg" class="form-control"  id="reply_msg" > <br>'
                }
                else {
                    document.getElementById('reply_msg').innerHTML = ''
                }
            });
            
        }
        
    }, false);
    $(document).ready(function () {
        $('#submitBtn').click(function() {
        checked = $("input[type=checkbox]:checked").length;

        if(!checked) {
            alert("You must check at least one checkbox.");
            return false;
        }

        });
    });
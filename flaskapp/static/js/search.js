// $('.datepicker').pickadate({
//     selectMonths: true, // Creates a dropdown to control month
//     selectYears: 100, // Creates a dropdown of 100 years to control year
//     format: 'yyyy-mm-dd'
// });
$("#student_id").prop("disabled", true);
$("#weight").prop("disabled", true);
$("#height").prop("disabled", true);
$("#sex").prop("disabled", true);
$("#exercise_name").prop("disabled", true);
$("#type").prop("disabled", true);
$("#intensity").prop("disabled", true);
        
$("input[name=use_student]").change(function() {
    if(this.checked) {
        $("#student_id").prop("disabled", false);
        $("#weight").prop("disabled", false);
        $("#height").prop("disabled", false);
        $("#sex").prop("disabled", false);
    } else {
        $("#student_id").prop("disabled", true);
        $("#weight").prop("disabled", true);
        $("#height").prop("disabled", true);
        $("#sex").prop("disabled", true);
    }
});

$("input[name=use_exercise]").change(function() {
    if(this.checked) {
        $("#exercise_name").prop("disabled", false);
        $("#type").prop("disabled", false);
        $("#intensity").prop("disabled", false);
    } else {
        $("#exercise_name").prop("disabled", true);
        $("#type").prop("disabled", true);
        $("#intensity").prop("disabled", true);
    }
});
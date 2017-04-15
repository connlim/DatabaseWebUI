//Disable all inputs by default
$("#student_id").prop("disabled", true);
$("#weight").prop("disabled", true);
$("#height").prop("disabled", true);
$("#sex").prop("disabled", true);
$("#exercise_name").prop("disabled", true);
$("#type").prop("disabled", true);
$("#intensity").prop("disabled", true);

//Enable/Disable inputs when the switches are changed
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

$(document).ready(function () {
    const formatYmd = date => date.toISOString().slice(0, 10);
    today=formatYmd(new Date());
    datenow = new Date();
    calcl_month = datenow.setMonth(datenow.getMonth() - 12);
    backdated = new Date(calcl_month).toISOString().slice(0, 10);
    
    calc_startyear = new Date().setFullYear(new Date().getFullYear() - 1, 0, 1);
    startyear = new Date(calc_startyear).toISOString().slice(0,10)

    calc_endyear = new Date().setFullYear(new Date().getFullYear() - 1, 11, 31);
    endyear = new Date(calc_endyear).toISOString().slice(0, 10)

    past5years = new Date();
    calc_fiveyear = past5years.setFullYear(past5years.getFullYear() - 5);
    fiveyear = new Date(calc_fiveyear).toISOString().slice(0, 10);

    $("#id_periodicity").change(function () {
        if ($(this).val()==1) {
            $("#id_start_period").val(today); //formatted current date returned by line 4   
            $("#id_end_period").val(today); //formatted current date returned by line 4

        } else if ($(this).val() == 2) {
            $("#id_start_period").val(today); //formatted current date returned by line 4 
            $("#id_end_period").val(today); //formatted current date returned by line 4 
        }
        
        else if ($(this).val() == 3) {
            $("#id_start_period").val(today); //formatted current date returned by line 4 
            $("#id_end_period").val(today); //formatted current date returned by line 4 
        }

        else if($(this).val() == 4) {
            $("#id_start_period").val(startyear); //computed delta calc_startyear line 10
            $("#id_end_period").val(endyear); //computed delta calc_endyear line 13
            $("#id_start_period").prop("readonly", true); //restrict editing
            $("#id_end_period").prop("readonly", true); //restrict editing
        }

        else if ($(this).val() == 5) {
            $("#id_start_period").val(fiveyear); //computed delta calc_fiveyear line 16
            $("#id_end_period").val(today);
            $("#id_start_period").prop("readonly", true); //restrict editing
            $("#id_end_period").prop("readonly", true); //restrict editing
        }

        else if ($(this).val() == 6) {
            $("#id_start_period").val(backdated); //computed delta last 12 months line 7
            $("#id_end_period").val(today); //formatted current date returned by line 4
            $("#id_start_period").prop("readonly", true); //restrict editing
            $("#id_end_period").prop("readonly", true); //restrict editing
        }

        else {
            $("#id_start_period").val(today); //formatted current date returned by line 4
            $("#id_end_period").val(today); //formatted current date returned by line 4
        }

    });
});
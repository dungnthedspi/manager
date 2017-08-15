$(document).ready(function() {
    var pathname = window.location.pathname.split( '/' );
    var student_id = pathname[pathname.length-1];
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
        defaultDate: new Date(),
        navLinks: true, // can click day/week names to navigate views
        editable: false,
        eventLimit: true, // allow "more" link when too many events
        events: {
            url: "/students/events",
            type: "POST",
            data: {
                student_id: student_id,
            },
        },
    });

});
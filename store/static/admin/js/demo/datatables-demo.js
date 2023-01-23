
$(document).ready(function() {
  $('#dataTable').DataTable({
    "language": {
"sProcessing": "Przetwarzanie ...",
"sLengthMenu": "Pokaż _MENU_ rekordów",
"sZeroRecords": "Żadne dane nie pasują do wprowadzonych",
"sEmptyTable": "Brak danych do wyświetlenia",
"sInfo": "Wyświetla od _START_ do _END_ z _TOTAL_",
"sInfoEmpty": "Nie znaleziono żadnych dopasowań",
"sInfoFiltered": "(filtrowano z _MAX_)",
"sInfoPostFix": "",
"sSearch": "Szukaj:",
"sUrl": "",
"sInfoThousands": ",",
"sLoadingRecords": "Wczytywanie rekordów..",
"oPaginate": {
  "sFirst": "Pierwszy", "sLast": "Ostatni", "sNext": "Następny", "sPrevious": "Poprzedni"
},
"oAria": {
  "sSortAscending": ": Sortuj rosnąco", "sSortDescending": ": Sortuj malejąco"
}
}
    });
});

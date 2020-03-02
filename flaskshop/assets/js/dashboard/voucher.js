import 'daterangepicker';
import './select';


$('#reservation').daterangepicker({
    autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      }
});

$('#reservation').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
});

$('#reservation').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});
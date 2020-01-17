import swal from 'sweetalert';
import './banner';

$(".delete-btn").click(
    function () {
        var $this = $(event.currentTarget)[0];
        var url = $($this).data('url');
        var redirect = $($this).data('redirect');
        swal({
            title: "Are you sure to delete?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    url: `/dashboard_api/${url}`,
                    type: 'DELETE',
                    data: {},
                    success: function (rs) {
                        if (rs.r) {
                            console.log(rs.msg)
                        } else {
                            swal("Poof! This item has been deleted!", {
                                icon: "success",
                            });
                            if (redirect) {
                                window.location.replace("/dashboard/products");
                            } else {
                                $this.closest('tr').remove();
                            }

                        }
                    }
                });
            }
        });
    }
)
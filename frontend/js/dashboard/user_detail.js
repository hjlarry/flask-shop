import swal from 'sweetalert';

$(".delete-btn").click(
    function () {
        var $this = $(event.currentTarget)[0];
        var url = $($this).data('url');
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
                            swal("Poof! This user has been deleted!", {
                                icon: "success",
                            });
                            window.location.replace("/dashboard/users");
                        }
                    }
                });
            }
        });
    }
);

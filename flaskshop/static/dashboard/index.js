const deleteItem = (delArgs, el) => {
    Swal.fire({
        title: 'Are you sure to delete?', icon: 'warning', showCancelButton: true, confirmButtonText: 'OK',
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/dashboard_api/${delArgs['delete-url']}`, {method: 'DELETE'}).then(res => {
                if (res.r) {
                    console.log(res.msg)
                } else {
                    Swal.fire("Poof! This item has been deleted!");
                    if (delArgs['redirect-url']) {
                        window.location.replace(delArgs['redirect-url']);
                    } else {
                        el.closest('tr').remove();
                    }

                }
            })
        }
    })
}

const delDirective = ({el, exp, effect}) => {
    effect(() => {
        el.addEventListener('click', () => {
            deleteItem(JSON.parse(exp), el)
        })
    })

}

PetiteVue.createApp().directive('delete', delDirective).mount()
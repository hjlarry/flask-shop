const toggleSidebarBtn = document.getElementById('toggleSidebar')

const toggleSibebar = () => {
    const isCollapse = document.body.classList.contains('sidebar-collapse')
    // 避免页面跳转时也呈现一个margin变化的动画
    const content = document.getElementById('content')
    content.classList.remove('no-transition')
    const header = document.getElementById('header')
    header.classList.remove('no-transition')
    if (isCollapse) {
        document.body.classList.remove('sidebar-collapse')
    } else {
        document.body.classList.add('sidebar-collapse')
    }
}
toggleSidebarBtn.addEventListener('click', toggleSibebar)


const toggleMenuBtns = document.querySelectorAll('.has-treeview')

const toggleMenu = (menu) => {
    const sub = menu.getElementsByClassName('nav-treeview')[0]
    const isOpen = menu.classList.contains('menu-open')
    if (isOpen) {
        sub.style.display = 'none'
        menu.classList.remove('menu-open')
    } else {
        sub.style.display = 'block'
        menu.classList.add('menu-open')
    }

}

toggleMenuBtns.forEach((menu) => {
    const callback = toggleMenu.bind(this, menu)
    menu.addEventListener('click', callback)
})

const deleteBtns = document.querySelectorAll('.delete-btn')

const deleteItem = (el) => {
    const deleteUrl = el.dataset.deleteUrl
    const redirectUrl = el.dataset.redirectUrl
    Swal.fire({
        title: 'Are you sure to delete?', icon: 'warning', showCancelButton: true, confirmButtonText: 'OK',
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/dashboard_api/${deleteUrl}`, {method: 'DELETE'}).then(res => {
                if (res.r) {
                    console.log(res.msg)
                } else {
                    Swal.fire("Poof! This item has been deleted!");
                    if (redirectUrl) {
                        window.location.replace(redirectUrl);
                    } else {
                        el.closest('tr').remove();
                    }
                }
            })
        }
    })
}

deleteBtns.forEach((btn) => {
    const callback = deleteItem.bind(this, btn)
    btn.addEventListener('click', callback)
})
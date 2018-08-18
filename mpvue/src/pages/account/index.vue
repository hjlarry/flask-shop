<template>
    <div class="page">
        <div class="page_head">
            <div class="userinfo-avatar">
                <open-data type="userAvatarUrl"></open-data>
            </div>

            <div class="userinfo-nickname">
                <open-data type="userNickName"></open-data>
            </div>
        </div>

        <div class="weui-panel">
            <div class="weui-panel__bd">
                <div class="weui-cells weui-cells_after-title">
                    <div class="weui-cell">
                        <div class="weui-cell__hd">
                            <image src="../../static/images/order.png"
                                   style="margin-right: 5px;vertical-align: middle;width:20px; height: 20px;" />
                        </div>
                        <div class="weui-cell__bd">My Order</div>
                        <div class="weui-cell__ft"> > </div>
                    </div>
                    <div class="weui-cell">
                        <div class="weui-cell__hd">
                            <image src="../../static/images/address.png"
                                   style="margin-right: 5px;vertical-align: middle;width:20px; height: 20px;" />
                        </div>
                        <div class="weui-cell__bd">My Address</div>
                        <div class="weui-cell__ft"> > </div>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<script>
    export default {

    };
</script>

<style>
    .page_head {
        display: flex;
        height: 30%;
        background-color: #1afa29;
        align-items: center;
    }

    .userinfo-avatar {
        clip-path: circle(30% at center);
    }

    .userinfo-nickname {
        color: #000000;
    }
</style>

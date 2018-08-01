<template>
    <div class="page">
        <div class="page__bd">
            <!-- 图文组合列表  start -->
            <div class="weui-panel weui-panel_access">
                <div class="weui-panel__hd">Featured Product</div>
                <div class="weui-panel__bd">
                    <navigator v-for="(item,index) in contentList" :key="index"
                               class="weui-media-box weui-media-box_appmsg" hover-class="weui-cell_active">
                        <div class="weui-media-box__hd weui-media-box__hd_in-appmsg">
                            <image class="weui-media-box__thumb" :src="item.first_img"/>
                        </div>
                        <div class="weui-media-box__bd weui-media-box__bd_in-appmsg">
                            <div class="weui-media-box__title">{{item.title}}</div>
                            <div class="weui-media-box__desc">{{item.description}}</div>
                        </div>
                    </navigator>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import base64 from '../../../static/images/base64';
    import Fly from 'flyio/dist/npm/wx';

    export default {
        data() {
            return {
                icon20: base64.icon20,
                icon60: base64.icon60,
                contentList: []
            }
        },
        methods: {
            getProductData: function () {
                wx.showLoading({
                    title: 'Loading Data',
                    mask: true
                })
                let fly = new Fly();
                fly.get('http://127.0.0.1:5000/api/v1/products/').then(res => {
                    wx.hideLoading()
                    this.contentList = res.data;
                })

            }
        },
        created() {
            this.getProductData()
        }
    }
</script>

<style>

</style>

<template>
    <div class="page">
        <div class="page__bd">
            <!-- 图文组合列表  start -->
            <div class="weui-panel weui-panel_access">
                <div class="weui-panel__hd">Featured Product</div>
                <div class="weui-panel__bd">
                    <navigator v-for="(item,index) in contentList" :key="index"
                               class="weui-media-box weui-media-box_appmsg" hover-class="weui-cell_active"
                               :url=" '/pages/product-detail/main?id='+item.id">
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
    import fly, {setTabBarBadge} from '@/utils/index'


    export default {
        data() {
            return {
                contentList: [],
                page: 1
            }
        },
        methods: {
            getProductData(page) {
                wx.showNavigationBarLoading()
                fly.get('products/', {page: page}).then(res => {
                    wx.hideNavigationBarLoading()
                    wx.stopPullDownRefresh()
                    this.contentList = this.contentList.concat(res.data);
                })
            }
        },
        onReachBottom() {
            this.page += 1
            this.getProductData(this.page)
        },
        onPullDownRefresh() {
            this.page = 1
            this.contentList = []
            this.getProductData(this.page)
        },
        mounted() {
            this.getProductData(this.page)
        },
        onShow() {
            setTabBarBadge()
        }
    }
</script>

<style>
</style>

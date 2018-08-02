<template>
    <div class="page">
        <div class="page__bd page__bd_spacing">
            <swiper :indicator-dots="indicatorDots" :autoplay="autoplay" :interval="interval" :duration="duration"
                    :circular="circular" @change="swiperChange" @animationfinish="animationfinish">
                <div v-for="item in product_content.images" :key="index">
                    <swiper-item>
                        <image :src="item" class="slide-image"/>
                    </swiper-item>
                </div>
            </swiper>
        </div>
    </div>
</template>

<script>
    import Fly from 'flyio/dist/npm/wx';

    export default {
        data() {
            return {
                indicatorDots: true,
                autoplay: true,
                interval: 5000,
                duration: 900,
                circular: true,
                product_content: {}
            }
        },
        methods: {
            getProductData: function (id) {
                wx.showLoading({
                    title: 'Loading Data',
                    mask: true
                })
                let fly = new Fly();
                fly.get('http://127.0.0.1:5000/api/v1/products/' + id).then(res => {
                    wx.hideLoading()
                    this.product_content = res.data;
                    console.log(res.data)
                })

            }
        },
        mounted() {
            console.log(this.$root.$mp.query)
            this.getProductData(this.$root.$mp.query.id)
        }
    }
</script>

<style>

</style>

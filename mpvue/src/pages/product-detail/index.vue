<template>
    <div class="page">
        <div class="page__bd page__bd_spacing">
            <swiper :indicator-dots="indicatorDots" :autoplay="autoplay" :interval="interval" :duration="duration"
                    :circular="circular" @change="swiperChange" @animationfinish="animationfinish">
                <div v-for="item in imgUrls" :key="index">
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
                imgUrls: [
                    'http://img02.tooopen.com/images/20150928/tooopen_sy_143912755726.jpg',
                    'http://img06.tooopen.com/images/20160818/tooopen_sy_175866434296.jpg',
                    'http://img06.tooopen.com/images/20160818/tooopen_sy_175833047715.jpg'
                ]
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
        mounted() {
            console.log(this.$root.$mp.query)
        },
        created() {

            // this.getProductData()
        }
    }
</script>

<style>

</style>

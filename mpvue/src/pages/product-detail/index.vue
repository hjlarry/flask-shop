<template>
    <div>
        <div class="page" :class="{ 'page_opacity': show_panel}">
            <div class="page__bd page__bd_spacing">
                <swiper :indicator-dots="indicatorDots" :autoplay="autoplay" :interval="interval" :duration="duration"
                        :circular="circular" @change="swiperChange" @animationfinish="animationfinish">
                    <div v-for="item in product_content.images" :key="index">
                        <swiper-item>
                            <image :src="item" class="slide-image"/>
                        </swiper-item>
                    </div>
                </swiper>
                <div class="weui-article">
                    <div class="weui-article__h1">{{product_content.title}}</div>
                    <div class="weui-article__section">
                        <div class="weui-article__section">
                            <div class="weui-article__p">
                                {{product_content.description}}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="weui-panel weui-panel_access">
                    <div class="weui-panel__hd">文字组合列表</div>
                    <div class="weui-panel__bd">
                        <div class="weui-cells weui-cells_after-title">
                            <radio-group @change="radioChange">
                                <label class="weui-cell weui-check__label" v-for="(item,index) in radioItems"
                                       :key="index">
                                    <radio class="weui-check" :value="item.value" :checked="item.checked"/>
                                    <div class="weui-cell__bd">{{item.name}}</div>
                                    <div class="weui-cell__ft weui-cell__ft_in-radio" v-if="item.checked">
                                        <icon class="weui-icon-radio" type="success_no_circle" size="16"></icon>
                                    </div>
                                </label>
                            </radio-group>
                            <div class="weui-cell weui-cell_link">
                                <div class="weui-cell__bd">添加更多</div>
                            </div>
                        </div>
                    </div>
                    <div class="weui-panel__ft">
                        <div class="weui-cell weui-cell_access weui-cell_link">
                            <div class="weui-cell__bd">查看更多</div>
                            <div class="weui-cell__ft weui-cell__ft_in-access"></div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="page__operation">
                <button class="weui-btn" type="primary" @click="showCartPanel">Add to Cart</button>
            </div>

        </div>
        <div class="panel" :class="{ 'show': show_panel}">

            <div class="weui-cell weui-cell_input">
                <div class="weui-cell__hd">
                    <div class="weui-label">qq</div>
                </div>
                <div class="weui-cell__bd">
                    <input class="weui-input" placeholder="请输入qq"/>
                </div>
            </div>
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
                show_panel: false,
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

            },
            showCartPanel() {
                this.show_panel = true
                console.log(111)
            }
        },
        mounted() {
            this.getProductData(this.$root.$mp.query.id)
        }
    }
</script>

<style>
    .page_opacity {
        opacity: 0.3
    }

    .panel {
        position: fixed;
        width: 100%;
        height: 400px;
        background-color: #ffffff;
        display: none;
    }

    .show {
        display: block;
    }

</style>

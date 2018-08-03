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
                    <div class="weui-article__h1">{{product_content.title}} <span class="right">${{product_content.price}}</span>
                    </div>
                    <div class="weui-article__section">
                        <div class="weui-article__section">
                            <div class="weui-article__p">
                                {{product_content.description}}
                            </div>
                        </div>
                    </div>
                </div>


            </div>
            <div class="page__operation">
                <button class="weui-btn" type="primary" @click="showCartPanel">Add to Cart</button>
            </div>

        </div>
        <div class="panel" :class="{ 'show': show_panel}">
            <div class="weui-panel weui-panel_access">
                <div class="weui-panel__bd">
                    <div class="weui-cell weui-cell_input">
                        <div class="weui-cell__hd">
                            <div class="weui-label">Quantity</div>
                        </div>
                        <div class="weui-cell__bd">
                            <input class="weui-input" :value="post_data.quantity"/>
                        </div>
                    </div>
                </div>
            </div>

            <div class="weui-panel weui-panel_access">
                <div class="weui-panel__hd">Choose Type <span class="right">${{variant_price}}</span></div>
                <div class="weui-panel__bd">
                    <div class="weui-cell weui-cell_input">
                        <div class="weui-cell__bd">
                            <button v-for="(item,index) in variant" class="weui-btn mini-btn" :type="item.button_type"
                                    :key="item.id" size="mini" @click="chooseVariant(index)">
                                {{item.title}}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <button class="weui-btn" type="primary" @click="postProductData">Add to Cart</button>
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
                variant_price: 0,
                product_content: {},
                variant: [],
                post_data: {
                    quantity: 1,
                    sku: ''
                }
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
                    this.variant = this.product_content.variant
                    this.variant.forEach(function (value) {
                        value.button_type = 'default'
                    })
                    this.chooseVariant(0)
                    console.log(res.data)
                })
            },
            showCartPanel() {
                this.show_panel = true
            },
            chooseVariant(index) {
                for (let i = 0; i < this.variant.length; ++i) {
                    let item = this.variant[i]
                    if (index === i) {
                        item.button_type = 'primary'
                        this.$set(this.variant, i, item);
                    } else {
                        item.button_type = 'default'
                        this.$set(this.variant, i, item);
                    }
                }
                this.variant_price = this.variant[index].price
                this.post_data.sku = this.variant[index].sku
            },
            postProductData: function () {
                wx.showLoading({
                    title: 'Loading Data',
                    mask: true
                })
                let fly = new Fly();
                fly.post('http://127.0.0.1:5000/api/v1/products/' + this.$root.$mp.query.id, this.post_data).then(res => {
                    console.log(res.data)
                })
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
        background-color: #eee;
        width: 95%;
        height: auto;
        margin: 0 auto;
        padding: 10px;
        overflow: hidden;
        position: fixed;
        bottom: 0;
        display: none;
    }

    .show {
        display: block;
    }


</style>

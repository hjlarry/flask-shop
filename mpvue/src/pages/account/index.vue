<template>
    <div class="page">
        
        <div class="animated infinite bounce delay-2s" style="background:red;height:100rpx;width:100rpx"></div>
        <h1 class="animated" :class="testcss">Example</h1>
        <button class="" @click="test1">test</button>

        

    </div>
</template>

<script>
export default {
  data: {
    animationData: {},
    test:false
  },
  computed:{
      testcss(){
          if (this.test){
              return 'fadeInUp'
          }else{
              return 'fadeOutDown'
          }
            
      }
  },
  methods:{
      test1(){
         this.test = !this.test
      }
  }
  
};
</script>

<style>
</style>

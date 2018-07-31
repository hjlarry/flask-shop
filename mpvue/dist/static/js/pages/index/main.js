global.webpackJsonp([5],{

/***/ 17:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0_vue___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_0_vue__);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__index__ = __webpack_require__(18);



const app = new __WEBPACK_IMPORTED_MODULE_0_vue___default.a(__WEBPACK_IMPORTED_MODULE_1__index__["a" /* default */]);
app.$mount();

/***/ }),

/***/ 18:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__babel_loader_node_modules_mpvue_loader_lib_selector_type_script_index_0_index_vue__ = __webpack_require__(20);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__node_modules_mpvue_loader_lib_template_compiler_index_id_data_v_6b277275_hasScoped_true_transformToRequire_video_src_source_src_img_src_image_xlink_href_node_modules_mpvue_loader_lib_selector_type_template_index_0_index_vue__ = __webpack_require__(24);
var disposed = false
function injectStyle (ssrContext) {
  if (disposed) return
  __webpack_require__(19)
}
var normalizeComponent = __webpack_require__(1)
/* script */

/* template */

/* styles */
var __vue_styles__ = injectStyle
/* scopeId */
var __vue_scopeId__ = "data-v-6b277275"
/* moduleIdentifier (server only) */
var __vue_module_identifier__ = null
var Component = normalizeComponent(
  __WEBPACK_IMPORTED_MODULE_0__babel_loader_node_modules_mpvue_loader_lib_selector_type_script_index_0_index_vue__["a" /* default */],
  __WEBPACK_IMPORTED_MODULE_1__node_modules_mpvue_loader_lib_template_compiler_index_id_data_v_6b277275_hasScoped_true_transformToRequire_video_src_source_src_img_src_image_xlink_href_node_modules_mpvue_loader_lib_selector_type_template_index_0_index_vue__["a" /* default */],
  __vue_styles__,
  __vue_scopeId__,
  __vue_module_identifier__
)
Component.options.__file = "src/pages/index/index.vue"
if (Component.esModule && Object.keys(Component.esModule).some(function (key) {return key !== "default" && key.substr(0, 2) !== "__"})) {console.error("named exports are not supported in *.vue files.")}
if (Component.options.functional) {console.error("[vue-loader] index.vue: functional components are not supported with templates, they should use render functions.")}

/* hot reload */
if (false) {(function () {
  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), false)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-6b277275", Component.options)
  } else {
    hotAPI.reload("data-v-6b277275", Component.options)
  }
  module.hot.dispose(function (data) {
    disposed = true
  })
})()}

/* harmony default export */ __webpack_exports__["a"] = (Component.exports);


/***/ }),

/***/ 19:
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 20:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__components_card__ = __webpack_require__(2);
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//



/* harmony default export */ __webpack_exports__["a"] = ({
  data() {
    return {
      motto: 'Hello World',
      userInfo: {}
    };
  },

  components: {
    card: __WEBPACK_IMPORTED_MODULE_0__components_card__["a" /* default */]
  },

  methods: {
    bindViewTap() {
      const url = '../logs/main';
      wx.navigateTo({ url });
    },
    getUserInfo() {
      // 调用登录接口
      wx.login({
        success: () => {
          wx.getUserInfo({
            success: res => {
              this.userInfo = res.userInfo;
            }
          });
        }
      });
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev);
    }
  },

  created() {
    // 调用应用实例的方法获取全局数据
    this.getUserInfo();
  }
});

/***/ }),

/***/ 24:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
var render = function () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;
  return _c('div', {
    staticClass: "container",
    attrs: {
      "eventid": '3'
    },
    on: {
      "click": function($event) {
        _vm.clickHandle('test click', $event)
      }
    }
  }, [_c('div', {
    staticClass: "userinfo",
    attrs: {
      "eventid": '0'
    },
    on: {
      "click": _vm.bindViewTap
    }
  }, [(_vm.userInfo.avatarUrl) ? _c('img', {
    staticClass: "userinfo-avatar",
    attrs: {
      "src": _vm.userInfo.avatarUrl,
      "background-size": "cover"
    }
  }) : _vm._e(), _vm._v(" "), _c('div', {
    staticClass: "userinfo-nickname"
  }, [_c('card', {
    attrs: {
      "text": _vm.userInfo.nickName,
      "mpcomid": '0'
    }
  })], 1)]), _vm._v(" "), _c('div', {
    staticClass: "usermotto"
  }, [_c('div', {
    staticClass: "user-motto"
  }, [_c('card', {
    attrs: {
      "text": _vm.motto,
      "mpcomid": '1'
    }
  })], 1)]), _vm._v(" "), _c('form', {
    staticClass: "form-container"
  }, [_c('input', {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: (_vm.motto),
      expression: "motto"
    }],
    staticClass: "form-control",
    attrs: {
      "type": "text",
      "placeholder": "v-model",
      "eventid": '1'
    },
    domProps: {
      "value": (_vm.motto)
    },
    on: {
      "input": function($event) {
        if ($event.target.composing) { return; }
        _vm.motto = $event.target.value
      }
    }
  }), _vm._v(" "), _c('input', {
    directives: [{
      name: "model",
      rawName: "v-model.lazy",
      value: (_vm.motto),
      expression: "motto",
      modifiers: {
        "lazy": true
      }
    }],
    staticClass: "form-control",
    attrs: {
      "type": "text",
      "placeholder": "v-model.lazy",
      "eventid": '2'
    },
    domProps: {
      "value": (_vm.motto)
    },
    on: {
      "change": function($event) {
        _vm.motto = $event.target.value
      }
    }
  })]), _vm._v(" "), _c('a', {
    staticClass: "counter",
    attrs: {
      "href": "/pages/counter/main"
    }
  }, [_vm._v("去往Vuex示例页面")]), _vm._v(" "), _c('a', {
    staticClass: "counter",
    attrs: {
      "href": "/pages/weui/main"
    }
  }, [_vm._v("ttt")])], 1)
}
var staticRenderFns = []
render._withStripped = true
var esExports = { render: render, staticRenderFns: staticRenderFns }
/* harmony default export */ __webpack_exports__["a"] = (esExports);
if (false) {
  module.hot.accept()
  if (module.hot.data) {
     require("vue-hot-reload-api").rerender("data-v-6b277275", esExports)
  }
}

/***/ })

},[17]);
//# sourceMappingURL=main.js.map
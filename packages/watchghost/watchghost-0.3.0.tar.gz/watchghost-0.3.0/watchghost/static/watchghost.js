var wsScheme = 'ws';
if (window.location.protocol == 'https:') {
  wsScheme = 'wss';
}
var wsLocation = wsScheme + "://" + window.location.host + "/websocket";

Vue.use(VueNativeSock.default, wsLocation, {
    format: 'json',
    reconnection: true
});
Vue.use(VueRouter);

Vue.component('watcher', {
  props: ['watcher', 'hide_info'],
  template: `
<li class="list-group-item" v-show="! (watcher.status === 'info' && hide_info)">
    <span v-if="watcher.status === 'info'" class="badge badge-pill badge-info text-monospace">I</span>
    <span v-else-if="watcher.status === 'warning'" class="badge badge-pill badge-warning text-monospace">W</span>
    <span v-else-if="watcher.status === 'error'" class="badge badge-pill badge-danger text-monospace">E</span>
    <span v-else-if="watcher.status === 'critical'" class="badge badge-pill badge-dark text-monospace">C</span>
    <span v-else="watcher.status === 'unknown'" class="badge badge-pill badge-light text-monospace border">?</span>
    <router-link 
        :to="{name: 'watcher-detail', params: {'uuid': watcher.uuid}}"
>
        {{ watcher.description }}
        <ul v-if="watcher.last_result && watcher.last_result.response.info">
          <li v-for="(value, key) in watcher.last_result.response.info">
              <strong>{{ key }}</strong>: {{ value }}
          </li>
        </ul>
    </router-link>
</li>`
});

Vue.component('group', {
  props: ['name', 'watchers', 'hide_info'],
  template: `
<div class="col-sm-6 col-md-4 col-lg-3">
<div class="card mb-3">
    <div v-if="name" class="card-header">
      {{ name }}
    </div>
    <div v-else class="card-header">
      Default
    </div>
    <ul class="list-group list-group-flush">
      <watcher
        v-for="watcher in watchers"
        :key="watcher.uuid" :hide_info="hide_info"
        v-bind:watcher="watcher"></watcher>
    </ul>
</div>
</div>
`})

const WatchersList = Vue.component('watchers_list', {
  props: ['watchers', 'tag', 'hide_info'],
  template: `
<div class="row">
    <group
        v-for="(object, uuid) in (tag ? by_tags : by_servers)"
        v-bind:name="object.name"
        v-bind:watchers="object.watchers"
        :key="uuid" :hide_info="hide_info"></group>
</div>`,
  computed: {
    by_servers: function() {
      return this.watchers.reduce(function(servers, watcher){
        if (!(watcher.server.uuid in servers)){
          servers[watcher.server.uuid] = {
            name: watcher.server.name,
            watchers: []
          }
        }
        servers[watcher.server.uuid].watchers.push(watcher);
        return servers;
      }, {});
    },
    by_tags: function() {
      tag = this.tag
      return this.watchers.reduce(function(tags, watcher){
        if (watcher.tags[tag]) {
          if (!(watcher.tags[tag] in tags)){
            tags[watcher.tags[tag]] = {
              name: watcher.tags[tag],
              watchers: []
            }
          }
          tags[watcher.tags[this.tag]].watchers.push(watcher);
          return tags;
        } else {
          return {};
        }
      }, {});
    }
  }
});

const WatcherDetail = Vue.component('watcher_detail', {
  props: ['watchers', 'uuid'],
  template: `
<dl v-if="watcher">
    <dt v-if="watcher.server.name">Server</dt>
    <dd v-if="watcher.server.name">{{ watcher.server.name }}</dd>
    <dt>Service</dt>
    <dd>{{ watcher.description }}</dd>
    <dt>Status</dt>
    <dd v-bind:class="{
          'bg-light': watcher.status == 'unknown',
          'bg-info text-light': watcher.status == 'info',
          'bg-warning text-light': watcher.status == 'warning',
          'bg-danger text-light': watcher.status == 'error',
          'bg-dark text-light': watcher.status == 'critical'}">
        {{ watcher.status }}
    </dd>
    <dt>Next check</dt>
    <dd>
      {{ next_check }}
      (<a href class="text-primary" @click.prevent="check_now">check now</a>)
    </dd>
    <dt v-if="watcher.last_result">Last result</dt>
    <dd v-if="watcher.last_result">
        <dl class="ml-4">
        <dt>Is hard</dt>
        <dd>{{ watcher.last_result.is_hard}}</dd>
        <dt>Start</dt>
        <dd>{{ watcher.last_result.start}}</dd>
        <dt>End</dt>
        <dd>{{ watcher.last_result.end}}</dd>
        <dt>Duration</dt>
        <dd>{{ duration }} ms</dd>

        <dt>Response</dt>
        <dd>
        <dl class="ml-4" v-for="(value, key) in watcher.last_result.response">
            <dt>{{ key }}</dt>
            <dd><pre>{{ value }}</pre></dd>
        </dl>
        </dd>
        </dl>
    </dd>
</dl>
<p v-else>Watcher not found</p>`,
  data: function(){
    return {now: Date.now(), interval_id: null}
  },
  computed: {
    watcher: function(){
      for (var i in this.watchers){
        var watcher = this.watchers[i];
        if(watcher.uuid == this.uuid){
            return watcher;
        }
      }
      return null;
    },
    duration: function(){
        if (this.watcher && this.watcher.last_result && this.watcher.last_result.start && this.watcher.last_result.end) {
        var start = new Date(this.watcher.last_result.start);
        var end = new Date(this.watcher.last_result.end);
        return end - start;
        }
        return null;
    },
    next_check: function(){
        if (this.watcher && this.watcher.next_check_hour){
            var check_hour = new Date(this.watcher.next_check_hour);
            var seconds = parseInt((check_hour - this.now) / 1000);
            if (seconds <= 0) return "checking";
            return seconds + ` second${seconds === 1 ? '' : 's'}`;
        }
        return null;
    }
  },
  mounted: function(){
    this.refresh_now();
  },
  beforeDestroy () {
    clearInterval(this.interval_id)
  },
  methods: {
    refresh_now: function(){
        this.interval_id = setInterval(function(){
          this.now = Date.now();
        }.bind(this), 1000);
    },
    check_now: function(){
        axios.get('/api/watchers/' + this.uuid + '/check_now/');
    }
  }
})

const router = new VueRouter({
  mode: 'history',
  routes: [
    {path: '/', component: WatchersList},
    {path: '/tag/:tag', component: WatchersList, props: true, name: 'tag'},
    {path: '/watchers/:uuid', component: WatcherDetail, props: true, name: 'watcher-detail'}
]});

var app = new Vue({
  router: router,
  el: '#app',
  template: `
<div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light rounded mb-2">
      <a class="navbar-brand" href="/">WatchGhost <small v-if="! ws_is_connected">(Disconnected)</small></a>
    </nav>
    <input type="checkbox" id="checkbox_hide_info" v-model="hide_info">
    <label for="checkbox_hide_info">Hide Info Status</label>
    <ul class="nav" v-if="tags">
      <li class="nav-item" v-for="tag in tags">
        <router-link :to="{name: 'tag', params: {'tag': tag}}" class="nav-link">{{ tag }}</router-link>
      </li>
    </ul>
    <router-view :watchers="watchers" :hide_info="hide_info" />
</div>
  `,
  data: {
    tags: [],
    watchers: [],
    ws_is_connected: false,
    hide_info: true
  },
  mounted() {
    this.ws_is_connected = this.$options.sockets.readyState === 1;
    this.$options.sockets.onopen = function(){
        this.ws_is_connected = true;
        axios.get('/api/watchers/').then(response => {
          this.watchers = response.data.objects;
          this.tags = this.watchers.reduce(
            function(tags, watcher){
              for (var tag in watcher.tags){
                if (!tags.includes(tag)) {
                  tags.push(tag);
                }
              }
              return tags;
            },
            []
          );
        });
    }
    this.$options.sockets.onmessage = (data) => {
      var message = JSON.parse(data.data);
      var data_uuid = Object.keys(message)[0];
      for (var i in this.watchers){
        var watcher = this.watchers[i];
        if(watcher.uuid === data_uuid){
          var new_watcher = JSON.parse(message[data_uuid]);
          this.watchers[i].status = new_watcher.status;
          this.watchers[i].next_check_hour = new_watcher.next_check_hour;
          this.watchers[i].last_result = new_watcher.last_result;
        }
      }
    };
    this.$options.sockets.onclose = function(){
        this.ws_is_connected = false;
        for(var i in this.watchers){
            var watcher = this.watchers[i];
            watcher.status = 'unknown';
            delete watcher.last_result;
            delete watcher.next_check_hour;
        }
    }
  },
})

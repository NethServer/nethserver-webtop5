<template>
  <div>
    <h2>{{$t('dashboard.title')}}</h2>
    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <div v-show="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-show="uiLoaded">
      <div class="row rowstats">
        <div class="content">
          <div class="stats-container col-xs-12 col-sm-6 col-md-4 col-lg-4">
            <span class="card-pf-utilization-card-details-count stats-count">{{configuration.active_users}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{$t('dashboard.active_users')}}</span>
            </span>
          </div>
          <div class="stats-container col-xs-12 col-sm-6 col-md-4 col-lg-4">
            <span class="card-pf-utilization-card-details-count stats-count">{{configuration.active_admins}}</span>
            <span class="card-pf-utilization-card-details-description stats-description">
              <span
                class="card-pf-utilization-card-details-line-2 stats-text"
              >{{$t('dashboard.active_admins')}}</span>
            </span>
          </div>
          <a
            target="_blank"
            :href="configuration.public_url"
            class="btn btn-primary btn-lg open-app"
          >{{$t('dashboard.open_app')}}</a>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-6 col-md-4 col-lg-4">
          <h3 class="space">{{ $t('dashboard.webtop_modules_version') }}</h3>
          <form class="form-horizontal">
            <span v-for="(item, key) in configuration.version" :key="key">
              <div class="form-group">
                <label class="col-sm-4 control-label">
                  {{$t('dashboard.webtop_' + key)}}
                </label>
                <div class="col-sm-5 item">
                  {{item}}
                </div>
              </div>
            </span>
          </form>
        </div>
      </div>
      <div v-show="configuration.admin_pass_warn" class="row">
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
          <h3 class="space">{{ $t('dashboard.webtop_admin_password') }}</h3>
          <div class="alert alert-warning">
            <span class="pficon pficon-warning-triangle-o"></span>
            <strong>{{$t('dashboard.warning')}}:</strong>
            {{$t('dashboard.change_default_password')}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  components: {
  },
  props: {
  },
  mounted() {
    this.getDashboardData()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      configuration: {
        active_users: 0,
        version: {},
        public_url: null,
        admin_pass_warn: false
      }
    };
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage
    },
    closeErrorMessage() {
      this.errorMessage = null
    },
    getDashboardData() {
      var context = this;
      context.uiLoaded = false;
      nethserver.exec(
        ["nethserver-webtop5/dashboard/read"],
        { action: "configuration" },
        null,
        function(success) {
          try {
            context.configuration = JSON.parse(success).configuration;
            
            var sorted = {};
            Object.keys(context.configuration.version).sort().forEach(function(key) {
              sorted[key] = context.configuration.version[key];
            });
            context.configuration.version = sorted;
            
            context.configuration.public_url = "http://" + window.location.host.split(":")[0] + "/webtop";
          } catch (e) {
            console.error(e);
          }
          context.uiLoaded = true;
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("dashboard.error_reading_webtop5_configuration"), error);
        }
      );
    }
  }
};
</script>

<style>
.stats-description-small {
  float: left;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 16px;
  font-weight: 300;
  line-height: 2;
}
.stats-text-small {
  line-height: 0.5;
}
.stats-count {
  font-size: 26px;
  font-weight: 300;
  margin-right: 10px;
  float: left;
  line-height: 1;
}
.rowstats {
  padding-left: 20px;
  padding-right: 20px;
}
.stats-text {
  margin-top: 10px !important;
  display: block;
}
.stats-description {
  float: left;
  line-height: 1;
}
.stats-container {
  padding: 20px !important;
  border-width: initial !important;
  border-style: none !important;
  border-color: initial !important;
  -o-border-image: initial !important;
  border-image: initial !important;
}
.stats-text {
  margin-top: 10px !important;
  display: block;
}
.stats-description {
  float: left;
  line-height: 1;
}
.stats-count {
  font-size: 26px;
  font-weight: 300;
  margin-right: 10px;
  float: left;
  line-height: 1;
}
.open-app {
  float: right;
  position: absolute;
  top: 16px;
  right: 20px;
}
.item {
  padding-top: 3px;
}
.space {
  margin-bottom: 25px;
}
</style>
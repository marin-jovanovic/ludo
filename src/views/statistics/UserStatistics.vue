<template>
  <base-user-template>
    <BaseMiddleContainer>
      <!-- <div>
        <h2>{{ playerName }} Statistics</h2>
        <div>
          <canvas ref="playedGamesChart" width="400" height="400"></canvas>
        </div>
        <div>
          <canvas ref="winsChart" width="400" height="400"></canvas>
        </div>
        <div>
          <canvas
            ref="resultDistributionChart"
            width="400"
            height="400"
          ></canvas>
        </div>
      </div> -->
      <base-chart ref="chart"></base-chart>

      <br />
      <hr />
      number of played levels: {{ this.levelsPlayed }}
      <hr />
      <br />
      number of quits: {{ this.cntQuits }}
      <hr />
      <br />

      <div v-for="(cnt, ind) in this.wins" :key="ind">
        place {{ ind }} : {{ cnt.length }}

        <hr />
        <br />
      </div>

      <ui-grid class="demo-grid">
        <ui-grid-cell
          style="border: 1px solid"
          class="demo-cell"
          columns="3"
          v-for="(user, index) in users"
          :key="index"
        >
          <ui-card class="demo-card demo-card--photo">
            <ui-card-content class="demo-card__primary-action">
              <ui-card-media square class="demo-card__media">
                <ui-card-media-content
                  class="demo-card__media-content--with-title"
                >
                  <div :class="[$tt('subtitle2'), 'demo-card__media-title']">
                    {{ user.name }}
                  </div>
                </ui-card-media-content>
              </ui-card-media>
            </ui-card-content>
            <ui-card-actions>
              <ui-card-icons>
                <ui-icon-button
                  :toggle="icon1"
                  @click="messageUser(index)"
                ></ui-icon-button>
              </ui-card-icons>
            </ui-card-actions>
          </ui-card>
        </ui-grid-cell>
      </ui-grid>
    </BaseMiddleContainer>
  </base-user-template>
</template>
          
        <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
// import { userConnectionApi } from "@/scripts/api/user_connection";
// import { userApi } from "@/scripts/api/user";
// import { userProfilePhoto } from "@/scripts/api/user_profile_photo";
import BaseMiddleContainer from "@/components/BaseMiddleContainer.vue";
import BaseChart from "@/components/BaseChart.vue";
import { statisticsApi } from "@/scripts/api/statistics";
import { router } from "@/router/router";

export default {
  data() {
    return {
      users: [],
      currentPage: 0,
      icon1: {
        off: "play_arrow",
        on: "stop",
      },

      levelsPlayed: undefined,
      wins: undefined,
      cntQuits: undefined,
      // icon2: {
      //   on: "add_circle",
      //   off: "add_circle_outline",
      // },
      // icon3: {
      //   on: "remove_circle",
      //   off: "remove_circle_outline",
      // },
    };
  },
  async mounted() {
    let res = await statisticsApi.getAllConnections();
    console.log(res);

    this.users = res["levelsPlayed"];

    this.levelsPlayed = res["numberOfPlayedLevels"];

    this.wins = res["wins"];
    this.cntQuits = res["quits"];

    let maxL = this.cntQuits;
    console.log("start", maxL);

    for (const [key, value] of Object.entries(this.wins)) {
      console.log(key, value);
      if (value.length > maxL) {
        maxL = value.length;
      }
    }

    // set row col

    console.log("max", maxL);
    this.$refs.chart.setColumn(maxL);

    for (let i = 0; i < this.cntQuits; i++) {
      // const element = array[i];:
      // 1stc
      // console.log("click",i);
      this.$refs.chart.oneClick("quit", 0, i);
    }

    let m = {
      0: "1st",
      1: "2nd",
      2: "3rd",
      3: "4th",
    };

    for (const [key, value] of Object.entries(this.wins)) {
      console.log(key);
      for (let i = 0; i < value.length; i++) {
        // console.log(m[key]);
        this.$refs.chart.oneClick(m[key], Number(key) + 1, i);
      }
    }

    // this.$refs.chart.oneClick("1st", 5, 3);
    // this.$refs.chart.oneClick("2nd", 2, 2);

    // await this.fetchUsers();

    // this.renderPlayedGamesChart();
    // this.renderWinsChart();
    // this.renderResultDistributionChart();
  },
  methods: {
    messageUser(levelId) {
      console.log("play level", levelId);

      // gameReplay/:id

      router.push(`gameReplay/${levelId}`);
    },
    // async addUser(userId) {
    //   userConnectionApi.sendConnectionRequest({ userId: userId });
    // },
    // async fetchUsers() {
    //   let t = await userApi.getAllUsers();
    //   console.log(t);
    //   this.users = t.users;
    //   for (const userId of Object.keys(this.users)) {
    //     let r = await userProfilePhoto.getProfilePhoto({ userId: userId });
    //     this.users[userId]["userProfilePhoto"] = r["userProfilePhoto"];
    //   }
    // },
    // async fetchMoreUsers() {
    //   this.fetchUsers();
    // },
  },
  components: {
    BaseUserTemplate,
    BaseMiddleContainer,
    BaseChart,
  },
};
</script>
     

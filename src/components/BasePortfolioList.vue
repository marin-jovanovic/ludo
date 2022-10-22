<template>
  <div>
    <BaseNotification ref="notification"></BaseNotification>
    <BaseMapOverlay ref=""></BaseMapOverlay>

    <div>
      <div class="col">
        <h1>Games</h1>
      </div>

      <div class="col col-lg-1">
        <button
          v-if="!this.isTempCreated"
          class="btn btn-primary"
          @click="createRow"
        >
          Add
        </button>
        <button v-else class="btn btn-secondary" disabled>Add</button>
      </div>

      <div class="col">selected: {{ selected }}</div>

      <hr />

      <br />

      <div v-for="portfolioPayload in this.portfolios" :key="portfolioPayload">
        <div class="row">
          {{ portfolioPayload }}
        </div>

        <div class="row">
          <div class="col">
            <input
              type="text"
              class="form-control"
              v-model="portfolioPayload.newName"
              placeholder="Portfolio name"
            />
          </div>

          <div v-if="portfolioPayload.isInDb" class="col">
            <button
              v-if="
                isNewName(portfolioPayload) || isNewColour(portfolioPayload)
              "
              @click="updatePortfolio(portfolioPayload)"
              class="btn btn-primary"
            >
              Update
            </button>

            <button v-else class="btn btn-secondary" disabled>Update</button>
          </div>
          <div v-else class="col">
            <button
              v-if="
                isNewName(portfolioPayload) && isNewColour(portfolioPayload)
              "
              @click="createPortfolio(portfolioPayload)"
              class="btn btn-primary"
            >
              Create
            </button>

            <button v-else class="btn btn-secondary" disabled>Create</button>
          </div>

          <div
            v-if="!portfolioPayload.isExpanded && portfolioPayload.isInDb"
            class="col"
          >
            <button
              @click="selectRow(portfolioPayload)"
              class="btn btn-primary"
            >
              Expand
            </button>
          </div>
          <div v-else-if="portfolioPayload.isInDb" class="col">
            <button
              @click="selectRow(portfolioPayload)"
              class="btn btn-primary"
            >
              Retract
            </button>
          </div>
        </div>

        <div v-show="portfolioPayload.isExpanded">
          <div class="row">row1</div>
          <div class="row">row2</div>
          <!-- <TheLocationTable
            @selectUpdate="updateSelectedList"
            @increase-by="updateSelectedForChart"
            @deleteLocation="deleteLocation"
            :portfolio="portfolioPayload.oldName"
            :t="this.locations[portfolioPayload.oldName]"
          >
            ></TheLocationTable
          > -->
        </div>

        <hr />
        <br />
      </div>
    </div>
  </div>
</template>
  

<script>
import { apiLobby } from "@/scripts/api/lobby";
// import TheLocationTable from "./TheLocationTable.vue";
import BaseNotification from "./BaseNotification.vue";

export default {
  props: {
    selectedForChart: Object,
  },
  data() {
    return {
      portfolios: {},
      isTempCreated: false,
      isContentCleared: false,
      locations: {},
      portfolioNamePlaceholder: "todo",
      portfolioColourPlaceholder: "todo",
      autoSave: false,
      selected: undefined,
      selectedSet: undefined,
    };
  },

  async mounted() {
    await this.loadPortfolios();
  },
  methods: {
    deleteLocation(pl) {
      // delete this.por
      console.log(pl);
      delete this.locations[pl.portfolio.oldName];
    },

    updateSelectedList(pl) {
      this.$emit("selectUpdate", pl);
    },
    updateSelectedForChart(pl) {
      this.$emit("increaseBy", pl);
    },
    async loadPortfolios() {
      let res = await apiLobby.getGames();
      console.log("load", res);
      if (res["auth"]["status"]) {
        this.portfolios = Object.values(res["payload"]["payload"]["full"]).map(
          (i) => {
            console.log(i);

            return this.castPortfolio(i.name, i.capacity, i.players, true);
          }
        );
      }

      this.showMessage(
        res["auth"]["status"],
        "Portfolios loaded successfully!",
        "Portfolios loading error!"
      );
    },
    castPortfolio(name, colour, isExpanded, isInDb) {
      return {
        newName: name,
        oldName: name,
        newColour: "#" + colour,
        oldColour: "#" + colour,
        isExpanded: isExpanded,
        isInDb: isInDb,

        isUpdated: false,
      };
    },
    setPortfolio(portfolio, name, colour, isExpanded, isInDb) {
      portfolio.newName = name;
      portfolio.oldName = name;
      portfolio.newColour = colour;
      portfolio.oldColour = colour;
      portfolio.isExpanded = isExpanded;
      portfolio.isInDb = isInDb;
      portfolio.isUpdated = false;
    },
    castLocation(section, type, lat, lon, name) {
      return {
        oldSection: section,
        newSection: section,
        oldType: type,
        newType: type,
        lat: lat,
        lon: lon,
        isSelected: false,
        oldName: name,
        newName: name,
      };
    },
    clearContentPortfolio(portfolioPayload) {
      console.log("todo clear content", portfolioPayload);
    },
    isNewColour(portfolioPayload) {
      return portfolioPayload.oldColour !== portfolioPayload.newColour;
    },
    isNewName(portfolioPayload) {
      return portfolioPayload.oldName !== portfolioPayload.newName;
    },
    createRow() {
      // todo check if append row to top
      this.portfolios.push(
        this.castPortfolio(
          this.portfolioNamePlaceholder,
          this.portfolioColourPlaceholder,
          false,
          false
        )
      );
      this.isTempCreated = true;
    },
    isPortfolioNameValid(name) {
      // todo check in backend if newname != oldname && newcolour != old
      return name && name.trim() !== "";
    },
    showMessage(test, success, fail) {
      this.$refs.notification.showMessage(test, success, fail);
    },
    async createPortfolio(portfolioPayload) {
      if (!this.isPortfolioNameValid(portfolioPayload.newName)) {
        this.showMessage(false, "", "portfolio name is not valid");
        return;
      }

      let r = await apiLobby.createGame(
        portfolioPayload.newName,
        portfolioPayload.newColour
      );

      this.showMessage(
        r["payload"]["status"],
        `Created ${portfolioPayload.newName}`,
        "Error creating"
      );

      if (r["payload"]["status"]) {
        this.setPortfolio(
          portfolioPayload,
          portfolioPayload.newName,
          portfolioPayload.newColour,
          false,
          true
        );

        // can create new
        this.isTempCreated = false;
      }
    },
    async updatePortfolio(portfolioPayload) {
      console.log("update");
      let params = {};
      if (this.isNewName(portfolioPayload)) {
        params["name"] = portfolioPayload.newName;
      }
      if (this.isNewColour(portfolioPayload)) {
        params["colour"] = portfolioPayload.newColour;
      }
      console.log(params);
      let r = await apiLobby.patchPortoflios(portfolioPayload.oldName, params);

      if (r["payload"]["status"]) {
        this.setPortfolio(
          portfolioPayload,
          portfolioPayload.newName,
          portfolioPayload.newColour,
          portfolioPayload.isExpanded,
          true
        );
      }

      this.showMessage(
        r["payload"]["status"],
        `Updated changes for  ${portfolioPayload.newName}`,
        "Error saving"
      );
    },
    async deletePortfolio(portfolioPayload) {
      if (portfolioPayload.newName === "") {
        //  assumption: trying to delete new portfolio
        console.log("new name is empty");
        return;
      }

      let isConfirmed = await this.$swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      });

      if (!isConfirmed.isConfirmed) {
        return;
      }

      let oldName = portfolioPayload.oldName;
      let r = await apiLobby.deletePortfolio(oldName);
      if (r["payload"]["status"]) {
        var index = this.portfolios.indexOf(portfolioPayload);
        this.portfolios.splice(index, 1);
      }
      console.log(r["payload"]);

      this.showMessage(
        r["payload"]["status"],
        `Deleted ${oldName}`,
        "Error deleting"
      );
    },
    async selectRow(portfolioPayload) {
      portfolioPayload.isExpanded = !portfolioPayload.isExpanded;
      let r = await apiLobby.getAllLocationsInPortfolio(
        portfolioPayload.oldName
      );
      if (r["payload"]["status"]) {
        this.locations[portfolioPayload.oldName] = Object.values(
          r["payload"]["content"]
        ).map((item) => {
          return this.castLocation(
            item.section,
            item.type,
            item.lat,
            item.lon,
            item.name
          );
        });
      } else {
        this.showMessage(false, "", "Error fetching data, contact admin");
      }
    },
  },
  components: {
    // TheLocationTable,
    BaseNotification,
  },
};
</script>
  
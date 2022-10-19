<template>
  <div>
    <br />

    <div class="row" v-for="locationPayload in t" :key="locationPayload">
      <div class="col">
        {{ locationPayload.oldName }}
      </div>

      <div class="col">
        <input
          class="form-check-input"
          type="checkbox"
          id="checkboxNoLabel"
          aria-label="..."
          v-model="locationPayload.isSelected"
          @change="checkboxChanged($event, locationPayload)"
        />
      </div>

      <div class="col">
        <input
          type="text"
          class="form-control"
          v-model="locationPayload.newSection"
          placeholder="Location section"
        />
      </div>

      <div class="col">
        <input
          type="text"
          class="form-control"
          v-model="locationPayload.newType"
          placeholder="Location type"
        />
      </div>

      <div class="col">
        <img
          @click="mapClicked(locationPayload)"
          src="assets/map/map.png"
          alt="img"
          class="img-fluid float-left"
          style="width: 50%; height: auto"
        />
      </div>

      <div class="col">
        <button
          v-if="isChanged(locationPayload)"
          @click="updateLocation(locationPayload)"
          class="btn btn-primary"
        >
          Update
        </button>

        <button v-else class="btn btn-secondary" disabled>Update</button>
      </div>

      <div class="col">
        <button
          class="btn btn-primary"
          @click="deleteLocation(locationPayload)"
        >
          Delete
        </button>
      </div>

      <div class="col">
        <router-link
          :to="{
            name: `chart`,
            params: {
              portfolio: portfolio,
              section: locationPayload.oldSection,
              type: locationPayload.oldType,
            },
          }"
          target="_blank"
        >
          Show charts
        </router-link>
      </div>

      <div class="col">
        <button @click="showGraph(locationPayload)">show graph</button>
      </div>

      <hr />
      <br />
    </div>
  </div>
</template>

<script>
import { apiLocation } from "@/scripts/api/location";

export default {
  props: {
    t: Object,
    portfolio: String,
  },
  data() {
    return {
      selected: {},
      selectedList: new Set(),
    };
  },
  methods: {
    checkboxChanged(e, locationPayload) {
      console.log("fire");
      let o = {
        section: locationPayload.oldSection,
        type: locationPayload.oldType,
      };

      if (locationPayload.isSelected) {
        console.log("add if not present");
        // add if not present
        if (!this.selectedList.has(o)) {
          console.log("not present");

          this.selectedList.add(o);
        }
      } else {
        console.log("remove if present");
        // remove if present
        if (this.selectedList.has(o)) {
          console.log(" present");

          this.selectedList.delete(o);
        }
      }

      console.log(this.selectedList);

      this.$emit("selectUpdate", {
        portfolio: this.portfolio,
        locationPayload: locationPayload,
      });
    },
    showGraph(locationPayload) {
      this.$emit("increaseBy", {
        portfolio: this.portfolio,
        section: locationPayload.oldSection,
        type: locationPayload.oldType,
      });
    },
    getSelected() {
      console.log("selected");
      // let se

      // todo rewrite as selected is dictionary, key = portfolio, value = list of section, type tuples
      this.selected = [];

      this.t.forEach((element) => {
        if (element.isSelected) {
          // todo what if names are updated for portfolio, section or type

          this.selected.push({
            portfolio: this.portfolio,
            section: this.oldSection,
            type: this.oldType,
          });
          console.log(this.portfolio, element.oldSection, element.oldType);
        }
      });

      console.table(this.selected);

      return this.selected;
    },

    updateSelected(locationPayload) {
      console.log("update selected", locationPayload);
    },

    mapClicked(locationPayload) {
      console.log("map clicked", locationPayload);
    },
    setPortfolioName() {
      console.log("todo parent portfolio name changed");
    },
    async deleteLocation(locationPayload) {
      console.log(locationPayload);
      //   if (
      //     !confirm(
      //       "Are you sure you want to delete " + portfolioPayload.newName + "?"
      //     )
      //   ) {
      //     return;
      //   }
      let r = await apiLocation.deleteLocation(
        this.portfolio,
        locationPayload.oldName
      );

      if (r["payload"]["status"]) {
        console.log("deleted, refresh site");

        // todo
        this.$emit("deleteLocation", {
          portfolio: this.portfolio,
          locationPayload: locationPayload,
        });

        // todo notify deleted
      } else {
        alert("error deleting");
        console.log("error delete");
      }
    },
    isChanged(locationPayload) {
      return (
        locationPayload.newSection !== locationPayload.oldSection ||
        locationPayload.oldType !== locationPayload.newType
      );
    },
    async updateLocation(locationPayload) {
      console.log("update");
      console.log(locationPayload);

      let params = {};

      //   todo click and drag drop UI
      params["section"] = locationPayload.newSection;
      params["type"] = locationPayload.newType;
      params["latitude"] = locationPayload.lat;
      params["longitude"] = locationPayload.lon;

      //   if (this.isNewName(portfolioPayload)) {
      //     params["name"] = portfolioPayload.newName;
      //   }
      //   if (this.isNewColour(portfolioPayload)) {
      //     params["colour"] = portfolioPayload.newColour;
      //   }
      console.log(params);
      let r = await apiLocation.patchLocation(
        this.portfolio,
        locationPayload.oldSection,
        locationPayload.oldType,
        params
      );
      if (r["payload"]["status"]) {
        console.log("location update done");
        //   this.showMessage("updated changes for " + "old name");
      } else {
        console.log("error saving");
      }
    },
  },
};
</script>

<style>
</style>
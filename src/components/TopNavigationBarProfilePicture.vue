<template>
  <img
    :src="this.profilePhoto"
    style="width: 50px; height: 50px; border-radius: 50%"
    :alt="this.username"
  />

  <!--     src="jpg/pexels-johannes-plenio-1103970.jpg"
 -->
</template>
    
  <script>
import { apiSettings } from "@/scripts/api/settings";
// import { userMetaSS } from "@/scripts/session_storage";
export default {
  data() {
    return { username: undefined, profilePhoto: undefined };
  },
  async mounted() {
    // this.profilePhoto = userMetaSS.getUserMeta()["userProfilePhoto"];

    // console.log(this.profilePhoto);

    let r = await apiSettings.getSettings();

    this.username = r["username"];

    this.profilePhoto = r["userProfilePhoto"];
  },
};
</script>
    
  <style>
</style>
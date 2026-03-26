import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.questly.app',
  appName: 'Questly',
  webDir: '.output/public',    // ← where Nuxt puts static build output
  server: {
    androidScheme: 'http'
  }
};

export default config;
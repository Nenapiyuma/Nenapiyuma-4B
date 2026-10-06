plugins { id("com.android.application"); id("org.jetbrains.kotlin.android"); id("org.jetbrains.kotlin.plugin.compose") }
android { namespace="com.nenapiyuma.fourb"; compileSdk=35
    defaultConfig { applicationId="com.nenapiyuma.fourb"; minSdk=26; targetSdk=35; versionCode=1; versionName="1.0" }
}
dependencies {
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.compose.ui:ui:1.7.8")
    implementation("androidx.compose.material3:material3:1.3.1")
}

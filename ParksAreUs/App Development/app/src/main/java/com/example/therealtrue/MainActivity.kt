package com.example.therealtrue
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.annotation.DrawableRes
import androidx.appcompat.content.res.AppCompatResources
import com.google.android.gms.location.SettingsClient
import com.mapbox.android.core.location.LocationEngine
import com.mapbox.android.core.permissions.PermissionsListener
import com.mapbox.android.core.permissions.PermissionsManager
import com.mapbox.common.location.Location
import com.mapbox.geojson.Point
import com.mapbox.maps.CameraOptions
import com.mapbox.maps.MapView
import com.mapbox.maps.MapboxMap
import com.mapbox.maps.Style
import com.mapbox.maps.plugin.animation.MapAnimationOptions
import com.mapbox.maps.plugin.animation.flyTo
import com.mapbox.maps.plugin.annotation.annotations
import com.mapbox.maps.plugin.annotation.generated.PointAnnotationOptions
import com.mapbox.maps.plugin.annotation.generated.createPointAnnotationManager
import com.mapbox.maps.plugin.gestures.OnMapClickListener
import com.mapbox.maps.plugin.gestures.gestures
import com.mapbox.maps.plugin.locationcomponent.location


class MainActivity : ComponentActivity(), PermissionsListener {

    private lateinit var mapView: MapView

    val REQUEST_CHECK_SETTINGS = 1
    var settingsClient: SettingsClient? = null

    lateinit var map: MapboxMap
    lateinit var permissionManager: PermissionsManager
    var originLocation: Location? = null

    var locationEngine: LocationEngine? = null


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity)
        mapView = findViewById(R.id.mapView)
        mapView.getMapboxMap().loadStyleUri(Style.SATELLITE_STREETS
        ) {
            mapView.location.updateSettings {
                enabled = true
                pulsingEnabled = true
            }
        }
        mapView.gestures.pitchEnabled = false

        newCameraPosition(Point.fromLngLat(54.3725, 24.4699))
        var captured : Point = Point.fromLngLat(12.0, 12.0)

        val mapClickListener = OnMapClickListener { point ->
            Toast.makeText(this@MainActivity, String.format("This is the Coordinates:%s %s", point.longitude().toString(), point.latitude().toString()),Toast.LENGTH_LONG).show()
            captured = point
            newCameraPosition(captured)
            true
        }
        mapView.gestures.addOnMapClickListener(mapClickListener)
        pythonCore(captured)
        annotationOnMap(captured)



    }

    private fun newCameraPosition(newPoint : Point){
        val cameraOptions = CameraOptions.Builder()
            .center(newPoint)
            .bearing(90.0)
            .pitch(0.0)
            .zoom(15.0)
            .build()

        val animationOptions = MapAnimationOptions.Builder().duration(15000).build()
        mapView.getMapboxMap().flyTo(cameraOptions, animationOptions)
    }

    private fun annotationOnMap(point : Point){
        val lng = point.longitude()
        val lat = point.latitude()
        // Create an instance of the Annotation API and get the PointAnnotationManager.
        bitmapFromDrawableRes(
            this@MainActivity,
            R.drawable.red_marker
        )?.let {
            val annotationApi = mapView.annotations
            val pointAnnotationManager = annotationApi.createPointAnnotationManager()
        // Set options for the resulting symbol layer.
            val pointAnnotationOptions: PointAnnotationOptions = PointAnnotationOptions()
        // Define a geographic coordinate.
                .withPoint(Point.fromLngLat(lng, lat))
        // Specify the bitmap you assigned to the point annotation
        // The bitmap will be added to map style automatically.
                .withIconImage(it)
        // Add the resulting pointAnnotation to the map.
            pointAnnotationManager.create(pointAnnotationOptions)
        }
    }

    private fun bitmapFromDrawableRes(context: Context, @DrawableRes resourceId: Int) =
        convertDrawableToBitmap(AppCompatResources.getDrawable(context, resourceId))

    private fun pythonCore(checker : Point){
        val lat = checker.latitude().toDouble()
        val long = checker.longitude().toDouble()
    }

    private fun convertDrawableToBitmap(sourceDrawable: Drawable?): Bitmap? {
        if (sourceDrawable == null) {
            return null
        }
        return if (sourceDrawable is BitmapDrawable) {
            sourceDrawable.bitmap
        } else {
// copying drawable object to not manipulate on the same reference
            val constantState = sourceDrawable.constantState ?: return null
            val drawable = constantState.newDrawable().mutate()
            val bitmap: Bitmap = Bitmap.createBitmap(
                drawable.intrinsicWidth, drawable.intrinsicHeight,
                Bitmap.Config.ARGB_8888
            )
            val canvas = Canvas(bitmap)
            drawable.setBounds(0, 0, canvas.width, canvas.height)
            drawable.draw(canvas)
            bitmap
        }
    }





    override fun onExplanationNeeded(permissionsToExplain: MutableList<String>?) {
        TODO("Not yet implemented")
    }

    override fun onPermissionResult(granted: Boolean) {
        TODO("Not yet implemented")
    }
}
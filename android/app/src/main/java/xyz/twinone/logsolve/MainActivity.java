package xyz.twinone.logsolve;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.flurgle.camerakit.CameraListener;
import com.flurgle.camerakit.CameraView;

public class MainActivity extends AppCompatActivity {


    private CameraView mCameraView;
    private ImageView mImageView;
    private Button mButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        mCameraView = (CameraView) findViewById(R.id.camera);
        mImageView = (ImageView) findViewById(R.id.image);
        mButton = (Button)findViewById(R.id.button);

        mButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("Main", "Click");
                takePicture();
            }
        });
        mImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("Main", "Click");
                mCameraView.setVisibility(View.VISIBLE);
                mImageView.setVisibility(View.GONE);
            }
        });


        mCameraView.setCameraListener(new CameraListener() {
            @Override
            public void onPictureTaken(byte[] picture) {
                super.onPictureTaken(picture);

                // Create a bitmap
                Bitmap result = BitmapFactory.decodeByteArray(picture, 0, picture.length);
                mImageView.setImageBitmap(result);
                mImageView.setVisibility(View.VISIBLE);
                mCameraView.setVisibility(View.GONE);

            }
        });
    }

    private void takePicture() {
        mCameraView.captureImage();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mCameraView.start();
    }

    @Override
    protected void onPause() {
        mCameraView.stop();
        super.onPause();
    }

}

from app.models.camera_model import Camera
from app.repositories.camera_repository import CameraRepository
from typing import List, Optional

class CameraService:
    def __init__(self):
        self.repository = CameraRepository()

    def create_camera(self, id: str, location: str, rtsp_url: str, status: str = "deactive", 
                     res_width: int = 1920, res_height: int = 1080, fps: int = 25) -> Camera:
        camera = Camera(
            id=id,
            location=location,
            rtsp_url=rtsp_url,
            status=status,
            res_width=res_width,
            res_height=res_height,
            fps=fps
        )
        return self.repository.create(camera)

    def get_all_cameras(self) -> List[Camera]:
        return self.repository.get_all()

    def get_camera_by_id(self, camera_id: str) -> Optional[Camera]:
        return self.repository.get_by_id(camera_id)

    def delete_camera(self, camera_id: str) -> bool:
        camera = self.get_camera_by_id(camera_id)
        if camera:
            return self.repository.delete(camera)
        return False

    def activate_camera(self, camera_id: str) -> bool:
        camera = self.get_camera_by_id(camera_id)
        if camera:
            camera.status = 'active'
            return self.repository.update(camera)
        return False

    def deactivate_camera(self, camera_id: str) -> bool:
        camera = self.get_camera_by_id(camera_id)
        if camera:
            camera.status = 'deactive'
            return self.repository.update(camera)
        return False

    def get_cameras_by_location(self, location: str) -> List[Camera]:
        return self.repository.find_by_location(location)

    def get_active_cameras(self) -> List[Camera]:
        return self.repository.find_active_cameras()

    def get_deactive_cameras(self) -> List[Camera]:
        return self.repository.find_deactive_cameras()

    def update_camera(self, camera_id: str, location: Optional[str] = None, 
                      res_width: Optional[int] = None, res_height: Optional[int] = None, fps: Optional[int] = None, 
                      status: Optional[str] = None) -> Optional[Camera]:
        """
        Update a camera's attributes. Only updates the fields that are provided.
        
        Args:
            camera_id (str): The ID of the camera to update
            location (str, optional): New location
            rtsp_url (str, optional): New RTSP URL
            res_width (int, optional): New resolution width
            res_height (int, optional): New resolution height
            fps (int, optional): New FPS value
            status (str, optional): New status ('active' or 'deactive')
            
        Returns:
            Camera: The updated camera object, or None if camera not found
        """
        camera = self.repository.get_by_id(camera_id)
        if not camera:
            return None
        if location is not None:
            camera.location = location
        if res_width is not None:
            camera.res_width = res_width
        if res_height is not None:
            camera.res_height = res_height
        if fps is not None:
            camera.fps = fps
        if status is not None:
            camera.status = status
        updated_camera = self.repository.update(camera)
        return updated_camera

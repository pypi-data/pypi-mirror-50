import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import mimetypes
import logging
import zipfile
import os
import base64

log = logging.getLogger(__name__)


def get_filepath(resource_id):
    '''
    Returns the path to the location of the file associated with
    the resource with the given resource ID.
    '''
    return "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
        "/" + resource_id[3:6] + "/" + resource_id[6:]


def encode_files(resource, username):
    '''
    This function is used when viewing a ZIP file to extract the files
    in the archive and pass their contents to the Papaya viewer. It
    extracts them all to a temporary directory structure, reads each file
    and encodes its contents in base64 (which Papaya can display), and appends
    those contents to a list that is returned to Papaya and used directly to
    display the DICOM directory. The function skips files that are not
    DICOM (i.e., they do not have a .dcm extension).
    '''
    encoded_data = []
    src = get_filepath(resource["id"])
    dst = "/var/lib/ckan/default/zip/" + username + "/" + resource["package_id"]
    # temporarily unzip the file
    try:
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extractall(dst)
    # return an empty string if this was called on a non-ZIP file
    except zipfile.BadZipfile:
        return ""
    dir_list = os.listdir(dst)
    for i in range(len(dir_list)):
        if dir_list[i][-4:] == ".dcm":
            try:
                with open(dst + "/" + dir_list[i], 'r') as f:
                    contents = f.read()
                    encoded_image = base64.encodestring(contents)
                    encoded_data.append(encoded_image)
            except IOError:
                continue
    # remove unzipped directory
    os.system(" ".join(("rm -r", dst)))
    return encoded_data


class PapayaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        mimetypes.add_type("DICOM", ".dcm")
        mimetypes.add_type("NIFTI", ".nii")

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'papaya')

    # IResourceView

    def info(self):
        return {'name': 'papaya',
                'title': toolkit._('Papaya Viewer'),
                'icon': 'cube',
                'default_title': toolkit._('Papaya Viewer'),
                'iframed': False
                }

    def can_view(self, data_dict):
        resource = data_dict['resource']
        return (resource.get('format').lower() in ['dicom', 'nifti', 'zip'])

    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return "papaya_view.html"

    def form_template(self, context, data_dict):
        return "papaya_form.html"

    # IResourceController

    def after_create(self, context, resource):
        '''
        Used to determine whether a file should have Papaya as a default view.
        NIFTI and single DICOM files will always be viewable with Papaya, but
        only some ZIP files have DICOM files; those that don't should not have
        Papaya as a default view. This function checks the filenames inside
        an uploaded ZIP archive and adds Papaya as a view for the resource if
        the archive contains any files with .dcm extensions.
        '''
        found_dcm = False
        if (resource["format"] == "ZIP"):
            src = get_filepath(resource["id"])
            with zipfile.ZipFile(src, 'r') as zip_ref:
                for item in zip_ref.namelist():
                    if item[-4:] == ".dcm":
                        found_dcm = True
                        break
        if found_dcm or resource["format"] == "DICOM" or resource["format"] == "NIFTI":
            toolkit.get_action('resource_view_create')(context, {
                                    'resource_id': resource['id'],
                                    'title': 'Papaya View',
                                    'view_type': 'papaya'
                                })
        return resource

    # ITemplateHelpers
    def get_helpers(self):
        return {'papaya_get_filepath': get_filepath,
                'papaya_encode_files': encode_files}

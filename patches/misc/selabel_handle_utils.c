#include "selabel_handle_utils.h"

void selabel_handle_set_rec_file(struct selabel_handle *rec, char *path) {
    if (rec->spec_files) {
        free(rec->spec_files);
    }

    rec->spec_files_len = 1;
    rec->spec_files = calloc(1, sizeof(*rec->spec_files));
    rec->spec_files[0] = path;
}